#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["platformdirs"]
# ///
"""
Normalize raw LLM source dumps into a common JSONL schema.

Reads:  $XDG_CACHE_HOME/localai-kith-2025/raw/<source>/...
Writes: $XDG_CACHE_HOME/localai-kith-2025/normalized/<source>/<date>.jsonl

Common record fields (all may be None):
  source            "huggingface" | "epoch"
  source_id         Stable id within the source (HF: org/name; Epoch: Model)
  name              Display name
  author            Organization / namespace
  release_date      ISO date (or YYYY-MM) when known
  license           License or accessibility label
  base_model        Parent model id if derived (finetune/quant/adapter/merge)
  lineage_relation  "finetune" | "quantized" | "adapter" | "merge" | None
  parameters        Parameter count (float) when source reports it
  url               Source URL
  tags              Source-native tags
  extra             Source-specific fields kept verbatim
  raw_source        Where this record came from (for traceability)

Examples:
  ./normalize.py hf
  ./normalize.py epoch
  ./normalize.py all --date 2026-05-18
"""

import argparse
import csv
import datetime
import json
import os
import re
import sys
from pathlib import Path

from platformdirs import user_cache_dir

APP_NAME = "localai-kith-2025"

KNOWN_LINEAGE_RELATIONS = {
    "finetune", "quantized", "adapter", "merge", "instruct",
}


# --- atomic JSONL writer ----------------------------------------------------

def write_jsonl_atomic(path: Path, records) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    n = 0
    with open(tmp, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    os.replace(tmp, path)
    return n


# --- Hugging Face -----------------------------------------------------------

def _parse_hf_base_model(tags):
    """Return (base_model_id, lineage_relation) parsed from base_model:* tags.

    HF often emits both `base_model:<id>` and `base_model:<rel>:<id>` for the
    same record; the relation-bearing tag is authoritative for the relation.
    """
    base, rel = None, None
    for t in tags:
        if not t.startswith("base_model:"):
            continue
        parts = t.split(":")
        # base_model:<rel>:<id>  (rel like finetune/quantized/adapter/merge)
        if len(parts) >= 3 and parts[1] in KNOWN_LINEAGE_RELATIONS:
            rel = parts[1]
            base = ":".join(parts[2:])
        # base_model:<id>   (no rel; only adopt if nothing better seen)
        elif len(parts) == 2 and not base:
            base = parts[1]
    return base, rel


def normalize_hf_record(rec: dict) -> dict:
    tags = rec.get("tags") or []
    license = next((t.split(":", 1)[1] for t in tags if t.startswith("license:")), None)
    base, rel = _parse_hf_base_model(tags)
    created = rec.get("createdAt") or ""
    return {
        "source": "huggingface",
        "source_id": rec.get("id"),
        "name": (rec.get("id") or "").split("/", 1)[-1] or None,
        "author": rec.get("author"),
        "release_date": created[:10] or None,
        "license": license,
        "base_model": base,
        "lineage_relation": rel,
        "parameters": None,  # not exposed at list level; derivable from cardData if fetched
        "url": f"https://huggingface.co/{rec['id']}" if rec.get("id") else None,
        "tags": tags,
        "extra": {
            "pipeline_tag": rec.get("pipeline_tag"),
            "library_name": rec.get("library_name"),
            "downloads": rec.get("downloads"),
            "likes": rec.get("likes"),
            "gated": rec.get("gated"),
            "last_modified": rec.get("lastModified"),
        },
        "raw_source": "huggingface-hub-api",
    }


def normalize_huggingface(cache_dir: Path, date: str) -> Path:
    src_dir = cache_dir / "raw" / "huggingface" / date
    if not src_dir.is_dir():
        sys.exit(f"no HF snapshot at {src_dir}")
    out = cache_dir / "normalized" / "huggingface" / f"{date}.jsonl"

    def gen():
        for page_path in sorted(src_dir.glob("models-*.json")):
            with open(page_path) as f:
                batch = json.load(f)
            for rec in batch:
                yield normalize_hf_record(rec)

    n = write_jsonl_atomic(out, gen())
    print(f"  hf: {n} records -> {out}", file=sys.stderr)
    return out


# --- Epoch AI ---------------------------------------------------------------

def _to_float(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except ValueError:
        return None


def normalize_epoch_row(row: dict) -> dict:
    name = (row.get("Model") or "").strip()
    base = (row.get("Base model") or "").strip() or None
    accessibility = (row.get("Model accessibility") or "").strip() or None
    open_weights = (row.get("Open model weights?") or "").strip() or None
    pub = (row.get("Publication date") or "").strip() or None
    return {
        "source": "epoch",
        "source_id": name or None,
        "name": name or None,
        "author": (row.get("Organization") or "").strip() or None,
        "release_date": pub,
        "license": accessibility,
        "base_model": base,
        # Epoch doesn't distinguish finetune/quant/merge; treat any parent
        # as a finetune-style derivation.
        "lineage_relation": "finetune" if base else None,
        "parameters": _to_float(row.get("Parameters")),
        "url": (row.get("Link") or "").strip() or None,
        "tags": [t.strip() for t in (row.get("Task") or "").split(",") if t.strip()],
        "extra": {
            "domain": (row.get("Domain") or "").strip() or None,
            "country": (row.get("Country (of organization)") or "").strip() or None,
            "organization_categorization": (row.get("Organization categorization") or "").strip() or None,
            "training_compute_flop": _to_float(row.get("Training compute (FLOP)")),
            "training_dataset_size": _to_float(row.get("Training dataset size (total)")),
            "open_model_weights": open_weights,
            "frontier_model": (row.get("Frontier model") or "").strip() or None,
            "confidence": (row.get("Confidence") or "").strip() or None,
            "reference": (row.get("Reference") or "").strip() or None,
        },
        "raw_source": "epoch-notable-ai-models",
    }


def normalize_epoch(cache_dir: Path, date: str) -> Path:
    src = cache_dir / "raw" / "epoch" / f"{date}-notable_ai_models.csv"
    if not src.is_file():
        sys.exit(f"no Epoch snapshot at {src}")
    out = cache_dir / "normalized" / "epoch" / f"{date}.jsonl"

    def gen():
        with open(src, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                yield normalize_epoch_row(row)

    n = write_jsonl_atomic(out, gen())
    print(f"  epoch: {n} records -> {out}", file=sys.stderr)
    return out


# --- date discovery ---------------------------------------------------------

DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def latest_date(cache_dir: Path, source: str) -> str | None:
    """Find the most recent snapshot date for a source by scanning raw/."""
    root = cache_dir / "raw" / {"hf": "huggingface", "epoch": "epoch"}[source]
    if not root.is_dir():
        return None
    candidates: set[str] = set()
    for p in root.iterdir():
        m = DATE_RE.search(p.name)
        if m:
            candidates.add(m.group(0))
    return max(candidates) if candidates else None


# --- dispatch ---------------------------------------------------------------

SOURCES = {
    "hf": ("huggingface", normalize_huggingface),
    "epoch": ("epoch", normalize_epoch),
}


def main():
    default_cache = Path(user_cache_dir(APP_NAME))
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", choices=list(SOURCES) + ["all"])
    parser.add_argument("--date", help="snapshot date YYYY-MM-DD (default: latest available)")
    parser.add_argument("--cache-dir", type=Path, default=default_cache,
                        help=f"cache dir (default: {default_cache})")
    args = parser.parse_args()

    sources = list(SOURCES) if args.source == "all" else [args.source]
    for s in sources:
        _, fn = SOURCES[s]
        date = args.date or latest_date(args.cache_dir, s)
        if not date:
            print(f"[{s}] no raw snapshots found, skipping", file=sys.stderr)
            continue
        print(f"[{s}] date={date}", file=sys.stderr)
        fn(args.cache_dir, date)


if __name__ == "__main__":
    main()
