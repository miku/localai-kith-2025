# Open models for AI applications

> [KI-Tage](https://ki-tage.webwirtschaft.net/) Halle (Saale), [Martin Czygan](https://de.linkedin.com/in/martin-czygan-58348842), 2025-11-21
> 11:30-13:00 [90min]

## Overview

* talk 10 minutes about the why (and why not)
* have 10 demos (about 5 minutes each) as input, up for discussion; all built with openly available models and run on own hardware
* generic ideas and outlook

## About me

* Software developer, working on projects at [Leipzig University
  Library](https://de.wikipedia.org/wiki/Universit%C3%A4tsbibliothek_Leipzig),
[Internet Archive](https://archive.org) and [Mistral](https://mistral.ai)
* Previously also consultant, author, lecturer

Since 2008 I try to live by the motto:

> "The key here is that no matter how agile you are as coders, [...] data is
> going to be more agile than code. Because you going to write the code
> yourself, but the data you can leverage." -- [Peter Norvig at Start School
> 2008](https://youtu.be/LNjJTgXujno?si=IweUD5YQlbZ7eTWw&t=185) (5.4K view; I
> watched it a few times!)

[![](static/norvig-2008.png)](https://youtu.be/LNjJTgXujno?si=IweUD5YQlbZ7eTWw&t=185)

## What is an open model?

* an LLM is just a file!

![](static/smollm2-360-head-s.webp)

Or weights as colors (cutout):

![](static/screenshot-2025-10-13-174543-hf-smollm2-binpic.png)

Model availability is not binary, there is a spectrum:

> We propose a framework to assess six levels of access to generative AI
> systems, from [The Gradient of Generative AI Release: Methods and
> Considerations](https://arxiv.org/pdf/2302.04844):

* fully closed
* gradual or staged access
* hosted access
* cloud-based or **API access**
* **downloadable access** and
* **fully open**.

## List of popular open weights models

* [Llama](https://www.llama.com/)
* [Mistral](https://docs.mistral.ai/getting-started/models/models_overview/#open-models)
* [Gemma](https://deepmind.google/models/gemma/)
* [Qwen](https://huggingface.co/Qwen)
* [DeepSeek](https://huggingface.co/deepseek-ai)
* [GPT-OSS](https://en.wikipedia.org/wiki/Products_and_applications_of_OpenAI#GPT-OSS)
* [Apertus](https://de.wikipedia.org/wiki/Apertus)

> Apertus wurde im September 2025 vorgestellt und gilt damit als das erste
> große Sprachmodell aus der Schweiz. Es ist vollständig als Open Source
> verfügbar; auch der Quellcode des Trainingsprozesses sowie die Trainingsdaten
> sind offengelegt. -- [Apertus](https://de.wikipedia.org/wiki/Apertus)

The ocean of models and the research landscape is vast.

![](static/model_evolution.png) (from 10/2023,
[Link](https://www.researchgate.net/figure/A-chronological-overview-of-large-language-models-LLMs-multimodal-and-scientific_fig2_373451304),
from [Examining User-Friendly and Open-Sourced Large GPT Models: A Survey on
Language, Multimodal, and Scientific GPT
Models](https://arxiv.org/abs/2308.14149))

As of 2025-10-13, popular model hosting site huggingface lists 2147127 models.

![](static/screenshot-2025-10-13-172823-hf-models.png)

And more:

|    |   index | Name                | Release date[a]    | License[c]                            |
|---:|--------:|:--------------------|:-------------------|:--------------------------------------|
|  0 |       1 | GPT-1               | June 2018          | MIT[4]                                |
|  1 |       2 | BERT                | October 2018       | Apache 2.0[7]                         |
|  2 |       3 | T5                  | October 2019       | Apache 2.0[12]                        |
|  3 |       4 | XLNet               | June 2019          | Apache 2.0[15]                        |
|  4 |       5 | GPT-2               | February 2019      | MIT[21]                               |
|  5 |       7 | GPT-Neo             | March 2021         | MIT[27]                               |
|  6 |       8 | GPT-J               | June 2021          | Apache 2.0                            |
|  7 |      15 | GPT-NeoX            | February 2022      | Apache 2.0                            |
|  8 |      19 | YaLM 100B           | June 2022          | Apache 2.0                            |
|  9 |      21 | BLOOM               | July 2022          | Responsible AI                        |
| 10 |      22 | Galactica           | November 2022      | CC-BY-NC-4.0                          |
| 11 |      24 | Llama               | February 2023      | Non-commercial research[e]            |
| 12 |      26 | Chameleon           | June 2024          | Non-commercial research[63]           |
| 13 |      27 | Cerebras-GPT        | March 2023         | Apache 2.0                            |
| 14 |      28 | Falcon              | March 2023         | Apache 2.0[68]                        |
| 15 |      31 | OpenAssistant[71]   | March 2023         | Apache 2.0                            |
| 16 |      34 | Llama 2             | July 2023          | Llama 2 license                       |
| 17 |      37 | Mistral 7B          | September 2023     | Apache 2.0                            |
| 18 |      39 | Grok 1[82]          | November 2023      | Apache 2.0                            |
| 19 |      41 | Mixtral 8x7B        | December 2023      | Apache 2.0                            |
| 20 |      42 | Mixtral 8x22B       | April 2024         | Apache 2.0                            |
| 21 |      43 | DeepSeek-LLM        | November 29, 2023  | DeepSeek License                      |
| 22 |      44 | Phi-2               | December 2023      | MIT                                   |
| 23 |      47 | Gemma               | February 2024      | Gemma Terms of Use[91]                |
| 24 |      49 | DBRX                | March 2024         | Databricks Open Model License[93][94] |
| 25 |      50 | Fugaku-LLM          | May 2024           | Fugaku-LLM Terms of Use[95]           |
| 26 |      51 | Phi-3               | April 2024         | MIT                                   |
| 27 |      52 | Granite Code Models | May 2024           | Apache 2.0                            |
| 28 |      53 | Qwen2               | June 2024          | Qwen License                          |
| 29 |      54 | DeepSeek-V2         | June 2024          | DeepSeek License                      |
| 30 |      55 | Nemotron-4          | June 2024          | NVIDIA Open Model License[101][102]   |
| 31 |      57 | Llama 3.1           | July 2024          | Llama 3 license                       |
| 32 |      59 | Mistral Large       | November 2024      | Mistral Research License              |
| 33 |      60 | Pixtral             | November 2024      | Mistral Research License              |
| 34 |      61 | DeepSeek-V3         | December 2024      | MIT                                   |
| 35 |      63 | DeepSeek-R1         | January 2025       | MIT                                   |
| 36 |      64 | Qwen2.5             | January 2025       | Qwen License                          |
| 37 |      65 | MiniMax-Text-01     | January 2025       | Minimax Model license                 |
| 38 |      71 | Llama 4             | April 5, 2025      | Llama 4 license                       |
| 39 |      73 | Qwen3               | April 2025         | Apache 2.0                            |
| 40 |      76 | GLM-4.5             | July 29, 2025      | MIT                                   |
| 41 |      77 | GPT-OSS             | August 5, 2025     | Apache 2.0                            |
| 42 |      80 | DeepSeek-V3.1       | August 21, 2025    | MIT                                   |
| 43 |      82 | DeepSeek-V3.2-Exp   | September 29, 2025 | MIT                                   |
| 44 |      83 | GLM-4.6             | September 30, 2025 | Apache 2.0                            |

Via: [scripts/scrape-llm-table.py](scripts/scrape-llm-table.py)

## Applications

Basic chat application, e.g. desktop, web, mobile that you can run on prem or
on your laptop, etc.

* [LMStudio](https://lmstudio.ai/)
* [ollama](https://ollama.com/)
* [AnythingLLM](https://anythingllm.com/)
* [Nomic GPT4All](https://www.nomic.ai/gpt4all), [Anleitung](https://www.htw-berlin.de/fileadmin/HTW/Zentral/LSC/Formulare/Lokale_Sprachmodelle_mit_GPT4All_nutzen.pdf.pdf)
* ...

## Why?

* privacy
* control (you reuse the model/file forever)
* LLM is already a black box ...

> In-context learning means language models learning to do new tasks, better
> predict tokens, or generally reduce their loss dur- ing the forward-pass at
> inference-time, without any gradient-based updates to the model’s parameters.

> How does in-context learning work? **While we don’t know for sure**, there
> are some intriguing ideas. -- [Speech and Language Processing, Jurafsky,
> Martin, 08/2025](https://web.stanford.edu/~jurafsky/slp3/ed3book_aug25.pdf)

* after hardware costs, lower cost to run

> on <2k EUR HW, ex. qwen25; 28M tokens/day (prompt eval), 4.3M tokens/day
> (eval; 30+ novels per day); depending on the provider you can pay up to EUR
> 50/day for this kind of throughput (this is a vague calculation, of course)

* customizations
* security research (open models will be used)

## Why not?

* less usable overall ("no instruction following", ...)
* fewer integrations and conveniences
* more expensive to start with
* security (cf. [Security Challenges in AI Agent Deployment: Insights from a
  Large Scale Public Competition](https://arxiv.org/pdf/2507.20526)

## Use case of shared infra

* can share into infra
* example: [chat-ai](https://github.com/gwdg/chat-ai), 700K users;
  [concept](https://kisski.gwdg.de/dok/grundversorgung.pdf) for AI basis
services for a regional scientific community; est. cost EUR 5-10M; for
projected 1M users that would amount to about EUR 5-10 per year per user.

![](/static/header_hu_21bbca9802774865.webp)

