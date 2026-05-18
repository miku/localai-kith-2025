#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai>=1.40"]
# ///
"""Parse free-text descriptions of LLMs into structured JSON records using an
OpenAI-compatible chat completions endpoint.

Examples:
    ./llmparse.py assets/ibm-llm-list.txt
    cat doc.txt | ./llmparse.py - --model nemotron3:33b
    ./llmparse.py doc.txt --base-url http://strix:11434/v1
"""

import argparse
import json
import os
import sys

from openai import OpenAI

SYSTEM_PROMPT = """\
You extract structured records about large language models (LLMs) from a
free-text document. Read the entire input and emit one record per distinct
model or model variant that is named in the text. Do not invent details: if a
field is not stated or strongly implied in the source, use null (or an empty
list / object as appropriate).

Each record must be a JSON object with these fields:

- name:         canonical model name as written in the source
                (e.g. "Claude Opus 4.5", "DeepSeek-V3", "Gemma 3 270M")
- version:      version identifier separable from the family name, or null
                (e.g. "4.5", "3.1")
- variant:      size / capability variant, or null
                (e.g. "mini", "Pro", "Thinking", "20B", "Flash-Lite")
- publisher:    organization that released the model
- license:      verbatim license string if stated (e.g. "Apache 2.0", "MIT",
                "custom Llama license"); null if not stated
- openness:     one of "open_weights", "open_source", "proprietary",
                or "unknown" -- pick based on what the source actually claims
- release_date: ISO-8601 (YYYY-MM-DD, YYYY-MM, or YYYY) if stated; null
                otherwise
- papers:       list of related paper titles or arXiv IDs explicitly
                referenced; [] if none
- links:        list of URLs explicitly mentioned for this model; [] if none
- notes:        one or two short sentences capturing the distinguishing facts
                (architecture, parameter counts, capabilities, controversies);
                keep it terse
- extras:       object with any other concrete facts worth keeping
                (e.g. {"total_params": "671B", "active_params": "37B",
                "context_length": "128k"}); {} if none

Return a single JSON object of the form:

    {"models": [ {...}, {...}, ... ]}

Output JSON only -- no prose, no markdown fences.
"""


def main() -> int:
    p = argparse.ArgumentParser(
        description="Extract structured LLM records from free text via an OpenAI-compatible endpoint.",
    )
    p.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Input file path, or '-' for stdin (default: stdin)",
    )
    p.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", "http://strix:11434/v1"),
        help="OpenAI-compatible base URL (default: %(default)s)",
    )
    p.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", "qwen3.6:latest"),
        help="Model identifier (default: %(default)s)",
    )
    p.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY", "ollama"),
        help="API key; many local servers accept any non-empty value",
    )
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument(
        "--timeout",
        type=float,
        default=1800.0,
        help="Request timeout in seconds (default: %(default)s)",
    )
    p.add_argument(
        "--num-ctx",
        type=int,
        default=None,
        help="Ollama context window override (sent via extra_body)",
    )
    p.add_argument(
        "--stream", action="store_true", help="Stream tokens to stderr as they arrive"
    )
    p.add_argument(
        "-o",
        "--output",
        default="-",
        help="Output file path, or '-' for stdout (default: stdout)",
    )
    args = p.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input) as f:
            text = f.read()

    if not text.strip():
        print("error: empty input", file=sys.stderr)
        return 2

    client = OpenAI(base_url=args.base_url, api_key=args.api_key, timeout=args.timeout)
    extra_body = {}
    if args.num_ctx is not None:
        extra_body["options"] = {"num_ctx": args.num_ctx}

    kwargs = dict(
        model=args.model,
        temperature=args.temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        extra_body=extra_body or None,
    )

    if args.stream:
        chunks = []
        stream = client.chat.completions.create(stream=True, **kwargs)
        for ev in stream:
            delta = ev.choices[0].delta.content if ev.choices else None
            if delta:
                sys.stderr.write(delta)
                sys.stderr.flush()
                chunks.append(delta)
        sys.stderr.write("\n")
        content = "".join(chunks)
    else:
        resp = client.chat.completions.create(**kwargs)
        content = resp.choices[0].message.content or ""

    try:
        data = json.loads(content)
        rendered = json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        print("warning: model returned non-JSON output; emitting raw", file=sys.stderr)
        rendered = content

    if args.output == "-":
        sys.stdout.write(rendered + "\n")
    else:
        with open(args.output, "w") as f:
            f.write(rendered + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
