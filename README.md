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

Or number as colors (cutout):

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

