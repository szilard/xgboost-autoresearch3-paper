# Bibliography verification for plan/references.bib

Date of check: 2026-10-07. Scope: every entry whose `note` contains "TO VERIFY" (18 entries; the
19th occurrence of the string is the provenance legend on line 9 of the file, not an entry), plus a
title check of all 46 `eprint` ids against their arXiv abstract pages. `references.bib` was NOT
edited; the corrected entries below are ready to paste.

Status key: VERIFIED = every existing field confirmed at the primary source (fields may have been
added); CORRECTED = an existing field was wrong, or venue details that were flagged as missing are
now filled in; COULD NOT OPEN = primary page unreachable, entry left unchanged.

Summary: 8 VERIFIED, 10 CORRECTED, 0 COULD NOT OPEN. (Some secondary pages were unreachable --
OpenReview forum pages behind a bot check, dl.acm.org 403, openai.com 403, X/Twitter -- and are
noted per entry; in every such case an alternative primary source was opened.)

---

## 1. arino2026identicalruns -- VERIFIED

Opened: https://arxiv.org/abs/2609.33812

Found: "Identical Runs, Different Results: Benchmarking AI Coding Agents on Open-Weight Models",
Eduardo Ariño de la Rubia (Central European University), Szilard Pafka (Epoch); v1 submitted
27 September 2026; primary cs.SE, secondary cs.LG; comments "22 pages, 6 figures, 18 tables".
Title, authors, id and month all match the entry. Added `primaryClass`.

```bibtex
@misc{arino2026identicalruns,
  title         = {Identical Runs, Different Results: Benchmarking {AI} Coding Agents on Open-Weight Models},
  author        = {Ari{\~n}o de la Rubia, Eduardo and Pafka, Szilard},
  year          = {2026},
  month         = sep,
  eprint        = {2609.33812},
  archivePrefix = {arXiv},
  primaryClass  = {cs.SE},
  url           = {https://arxiv.org/abs/2609.33812},
  note          = {[V-SUB] 2026-10-07 arXiv abstract page (v1, 27 Sep 2026); cite by design only, no results}
}
```

## 2. pafka2015benchmml -- VERIFIED

Opened: https://github.com/szilard/benchm-ml ; GitHub API `repos/szilard/benchm-ml`

Found: repository About text: "A minimal benchmark for scalability, speed and accuracy of commonly
used open source implementations (R packages, Python scikit-learn, H2O, xgboost, Spark MLlib etc.)
of the top machine learning algorithms for binary classification (random forests, gradient boosted
trees, deep neural networks etc.)." README heading: "Simple/limited/incomplete benchmark for
scalability, speed and accuracy of machine learning libraries for classification". Repository
created 2015-03-28 (API `created_at`); README: "When I started this benchmark in March 2015".
Licence MIT. README: "Training datasets of sizes 10K, 100K, 1M, 10M are generated from the
well-known airline dataset (using years 2005 and 2006)." The bib title is the About text with the
two parentheticals removed; year 2015 confirmed. Added `month = mar`.

```bibtex
@misc{pafka2015benchmml,
  title        = {benchm-ml: A minimal benchmark for scalability, speed and accuracy of commonly used open source implementations of the top machine learning algorithms for binary classification},
  author       = {Pafka, Szilard},
  year         = {2015},
  month        = mar,
  howpublished = {GitHub repository},
  url          = {https://github.com/szilard/benchm-ml},
  note         = {[V-SUB] 2026-10-07 GitHub repository page and API (created 28 Mar 2015, MIT); title is the About text without its parentheticals; origin of the airline-delay 0.1M/1M/10M slices}
}
```

## 3. karpathy2026autoresearch -- CORRECTED (release date)

Opened: https://github.com/karpathy/autoresearch ; raw README
(https://raw.githubusercontent.com/karpathy/autoresearch/master/README.md) ; GitHub API
`repos/karpathy/autoresearch` and `.../commits?per_page=100`

Found: About text exactly "AI agents running research on single-GPU nanochat training
automatically" (matches the bib title). README section "## License" reads "MIT"; note that
GitHub's licence detector reports none (no separate LICENSE file), so the licence rests on the
README. README confirms `program.md` and "a fixed 5-minute time budget" per experiment and the
narrative line signed "-@karpathy, March 2026". Release date from the primary source: repository
`created_at` 2026-03-06T22:00:43Z; first commit b11d6f2 "initial commit" 2026-03-06T21:58:52Z
(36 commits in total, latest 2026-03-26). The "7 March 2026" in the old note comes from press
coverage of the announcement tweets (https://x.com/karpathy/status/2029701092347630069, linked
from the README; X could not be opened). Correction: first commit is 6 March 2026 (UTC).

```bibtex
@misc{karpathy2026autoresearch,
  title        = {autoresearch: {AI} agents running research on single-{GPU} nanochat training automatically},
  author       = {Karpathy, Andrej},
  year         = {2026},
  month        = mar,
  howpublished = {GitHub repository},
  url          = {https://github.com/karpathy/autoresearch},
  note         = {[V-SUB] 2026-10-07 GitHub repository, README and API; MIT per README; program.md and a fixed 5-minute budget per experiment; first commit 6 Mar 2026 (UTC), announced on X 7 Mar 2026}
}
```

## 4. openai2026codex -- CORRECTED (split into software release + configuration reference)

Opened: https://github.com/openai/codex/releases/tag/rust-v0.160.0 ; GitHub API
`repos/openai/codex/releases/tags/rust-v0.160.0` and `repos/openai/codex` ;
https://developers.openai.com/codex/config-reference (308 redirect) ->
https://learn.chatgpt.com/docs/config-file/config-reference

Found: release tag `rust-v0.160.0`, release title "0.160.0", `published_at` 2026-10-01T20:19:13Z,
published by andrewgu-oai, not a pre-release. Repository description "Lightweight coding agent that
runs in your terminal", licence Apache-2.0. Configuration reference: H1 "Configuration Reference",
site header "ChatGPT Learn", intro "Complete reference for Codex config.toml and requirements.toml";
in the `config.toml` table the `model_reasoning_effort` row (type string) reads verbatim:
"Reasoning effort advertised by the selected model, such as `low`, `medium`, `high`, `xhigh`,
`max`, or `ultra`. Available levels depend on the model and client." No version or last-updated
date is printed on that page. (For the paper: the GPT-6 model pages list `max` as the highest
level; `ultra` appears only in this generic list.)

```bibtex
@misc{openai2026codex,
  title        = {Codex {CLI}, version 0.160.0},
  author       = {{OpenAI}},
  year         = {2026},
  month        = oct,
  howpublished = {Software release rust-v0.160.0, GitHub},
  url          = {https://github.com/openai/codex/releases/tag/rust-v0.160.0},
  note         = {[V-SUB] 2026-10-07 GitHub release page and API (published 1 Oct 2026, Apache-2.0); the version used in every run}
}

@misc{openai2026codexconfig,
  title        = {Codex Configuration Reference},
  author       = {{OpenAI}},
  year         = {2026},
  howpublished = {Developer documentation, config.toml reference},
  url          = {https://developers.openai.com/codex/config-reference},
  note         = {[V-SUB] 2026-10-07 page (redirects to learn.chatgpt.com/docs/config-file/config-reference); model\_reasoning\_effort: ``low, medium, high, xhigh, max, or ultra''; accessed 7 Oct 2026}
}
```

## 5. openai2026gpt6 -- CORRECTED (official URLs, prices, effort levels, dates found)

Opened: https://developers.openai.com/api/docs/models/gpt-6-astra ;
https://developers.openai.com/api/docs/models/gpt-6-sol ;
https://developers.openai.com/api/docs/models/gpt-6-luna ;
https://developers.openai.com/api/docs/pricing (cross-check) ;
https://deploymentsafety.openai.com/gpt-6-astra/sec:appendix-sol-luna (system card, for dates) ;
https://community.openai.com/t/announcing-gpt-6-sol-and-gpt-6-luna-in-the-api-codex-and-chatgpt/1399925
and https://community.openai.com/t/introducing-gpt-6-astra-the-most-intelligent-and-aligned-model-in-the-world/1394703
(OpenAI developer forum, for dates). openai.com announcement pages returned HTTP 403.

Found, as printed on the model pages (all accessed 2026-10-07; prices per 1M tokens, standard tier):

| Model | Snapshot | Tagline | Input | Cached input | Output | Cache writes | `reasoning.effort` supports | Context / max output | Knowledge cutoff |
|---|---|---|---|---|---|---|---|---|---|
| GPT-6 Astra | `gpt-6-astra` | "Our most capable model for the most demanding work." | $10 | $1 | $50 | $12.5 | `low`, `medium`, `high`, `xhigh`, and `max` (no `none`; no default marked) | 1,050,000 / 128,000 | Apr 30, 2026 |
| GPT-6 Sol | `gpt-6-sol` | "Built to power complex coding and agentic workflows." | $2 | $0.2 | $10 | $2.5 | `none`, `low`, `medium` (default), `high`, `xhigh`, and `max` | 1,050,000 / 128,000 | Apr 20, 2026 |
| GPT-6 Luna | `gpt-6-luna` | "Our most efficient model for focused, high-volume tasks." | $0.1 | $0.01 | $0.5 | $0.125 | `none`, `low`, `medium` (default), `high`, `xhigh`, and `max` | 1,050,000 / 128,000 | May 18, 2026 |

The pricing page lists the same three numbers per model under "Short context" (standard tier).
Release dates are not on the model pages; the GPT-6 Astra System Card prints "Published
September 3, 2026" and its changelog adds Sol and Luna on September 22, 2026; the OpenAI forum
announcements are dated 3 Sep 2026 (Astra) and 22 Sep 2026 (Sol and Luna, posted by OpenAI staff).
This confirms the dates the old note took from press coverage.

Option A, one combined entry (same key):

```bibtex
@misc{openai2026gpt6,
  title        = {{GPT-6} model family: {GPT-6} {Astra}, {GPT-6} {Sol} and {GPT-6} {Luna}},
  author       = {{OpenAI}},
  year         = {2026},
  howpublished = {Model documentation, OpenAI API reference},
  url          = {https://developers.openai.com/api/docs/models/gpt-6-astra},
  note         = {[V-SUB] 2026-10-07 model pages gpt-6-astra, gpt-6-sol, gpt-6-luna (accessed 7 Oct 2026). List prices per 1M tokens (input / cached input / output): Astra \$10 / \$1 / \$50; Sol \$2 / \$0.20 / \$10; Luna \$0.10 / \$0.01 / \$0.50. reasoning.effort: Astra low, medium, high, xhigh, max; Sol and Luna none, low, medium (default), high, xhigh, max. Released 3 Sep 2026 (Astra) and 22 Sep 2026 (Sol, Luna) per the GPT-6 Astra System Card}
}
```

Option B, one entry per model:

```bibtex
@misc{openai2026gpt6astra,
  title        = {{GPT-6} {Astra}},
  author       = {{OpenAI}},
  year         = {2026},
  month        = sep,
  howpublished = {Model documentation, OpenAI API reference},
  url          = {https://developers.openai.com/api/docs/models/gpt-6-astra},
  note         = {[V-SUB] 2026-10-07 model page (accessed 7 Oct 2026): \$10 input, \$1 cached input, \$50 output per 1M tokens; reasoning.effort low, medium, high, xhigh, max; released 3 Sep 2026 per the system card}
}

@misc{openai2026gpt6sol,
  title        = {{GPT-6} {Sol}},
  author       = {{OpenAI}},
  year         = {2026},
  month        = sep,
  howpublished = {Model documentation, OpenAI API reference},
  url          = {https://developers.openai.com/api/docs/models/gpt-6-sol},
  note         = {[V-SUB] 2026-10-07 model page (accessed 7 Oct 2026): \$2 input, \$0.20 cached input, \$10 output per 1M tokens; reasoning.effort none, low, medium (default), high, xhigh, max; released 22 Sep 2026 per the system card}
}

@misc{openai2026gpt6luna,
  title        = {{GPT-6} {Luna}},
  author       = {{OpenAI}},
  year         = {2026},
  month        = sep,
  howpublished = {Model documentation, OpenAI API reference},
  url          = {https://developers.openai.com/api/docs/models/gpt-6-luna},
  note         = {[V-SUB] 2026-10-07 model page (accessed 7 Oct 2026): \$0.10 input, \$0.01 cached input, \$0.50 output per 1M tokens; reasoning.effort none, low, medium (default), high, xhigh, max; released 22 Sep 2026 per the system card}
}
```

## 6. zhang2023llmhpo -- CORRECTED (workshop venue added)

Opened: https://arxiv.org/abs/2312.04528 ; https://neurips.cc/virtual/2023/82901 ;
https://openreview.net/forum?id=FUdZ6HEOre (blocked by a browser check; id taken from the
neurips.cc page)

Found: arXiv v1 7 Dec 2023, v2 11 Nov 2024, comments "28 pages", no journal-ref, cs.LG. The
NeurIPS 2023 virtual site lists the paper (Michael Zhang, Nishkrit Desai, Juhan Bae, Jonathan
Lorraine, Jimmy Ba) under the workshop "Foundation Models for Decision Making", linking to
OpenReview id FUdZ6HEOre. No archival proceedings, so it stays a workshop paper.

```bibtex
@inproceedings{zhang2023llmhpo,
  title         = {Using Large Language Models for Hyperparameter Optimization},
  author        = {Zhang, Michael R. and Desai, Nishkrit and Bae, Juhan and Lorraine, Jonathan and Ba, Jimmy},
  booktitle     = {NeurIPS 2023 Workshop on Foundation Models for Decision Making},
  year          = {2023},
  eprint        = {2312.04528},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://arxiv.org/abs/2312.04528},
  note          = {[V-SUB] 2026-10-07 arXiv abstract page (v2 11 Nov 2024) and neurips.cc/virtual/2023/82901; OpenReview id FUdZ6HEOre}
}
```

## 7. huang2024mlagentbench -- CORRECTED (ICML 2024 venue completed)

Opened: https://arxiv.org/abs/2310.03302 ; https://proceedings.mlr.press/v235/huang24y.html

Found: arXiv v1 5 Oct 2023, v2 14 Apr 2024, cs.LG. PMLR: Proceedings of the 41st International
Conference on Machine Learning, PMLR 235:20271-20309, 2024; editors Salakhutdinov, Kolter, Heller,
Weller, Oliver, Scarlett, Berkenkamp. Title and authors identical.

```bibtex
@inproceedings{huang2024mlagentbench,
  title         = {{MLAgentBench}: Evaluating Language Agents on Machine Learning Experimentation},
  author        = {Huang, Qian and Vora, Jian and Liang, Percy and Leskovec, Jure},
  booktitle     = {Proceedings of the 41st International Conference on Machine Learning},
  series        = {Proceedings of Machine Learning Research},
  volume        = {235},
  pages         = {20271--20309},
  publisher     = {PMLR},
  year          = {2024},
  eprint        = {2310.03302},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://proceedings.mlr.press/v235/huang24y.html},
  note          = {[V-SUB] 2026-10-07 PMLR v235 page (huang24y) and arXiv abstract page}
}
```

## 8. jing2025dsbench -- CORRECTED (ICLR 2025 pages and proceedings URL added)

Opened: https://arxiv.org/abs/2409.07703 ; https://www.iclr.cc/virtual/2025/poster/30458 ;
https://proceedings.iclr.cc/paper_files/paper/2025/hash/50e9ad960ae78b741a6b4fea533f2eaf-Abstract-Conference.html
and its BibTeX (https://proceedings.iclr.cc/paper_files/paper/3590-/bibtex) ;
https://openreview.net/forum?id=DSsSPr0RZJ (blocked by a browser check; id from the iclr.cc page)

Found: arXiv v1 12 Sep 2024, v2 22 Feb 2025, v3 11 Apr 2025, cs.AI. ICLR 2025 Poster; proceedings
BibTeX: booktitle International Conference on Learning Representations, volume 2025, pages
32597--32649, editors Y. Yue, A. Garg, N. Peng, F. Sha, R. Yu. Title and nine authors identical.

```bibtex
@inproceedings{jing2025dsbench,
  title         = {{DSBench}: How Far Are Data Science Agents from Becoming Data Science Experts?},
  author        = {Jing, Liqiang and Huang, Zhehui and Wang, Xiaoyang and Yao, Wenlin and Yu, Wenhao and Ma, Kaixin and Zhang, Hongming and Du, Xinya and Yu, Dong},
  booktitle     = {International Conference on Learning Representations (ICLR)},
  pages         = {32597--32649},
  year          = {2025},
  eprint        = {2409.07703},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  url           = {https://proceedings.iclr.cc/paper_files/paper/2025/hash/50e9ad960ae78b741a6b4fea533f2eaf-Abstract-Conference.html},
  note          = {[V-SUB] 2026-10-07 ICLR 2025 proceedings page and BibTeX, iclr.cc poster page (OpenReview DSsSPr0RZJ), arXiv abstract page}
}
```

## 9. ouyang2024nondeterminism -- CORRECTED (volume, issue, pages added)

Opened: https://arxiv.org/abs/2308.02828 ; https://api.crossref.org/works/10.1145/3697010 ;
https://dl.acm.org/doi/10.1145/3697010 (HTTP 403)

Found: Crossref: "An Empirical Study of the Non-Determinism of ChatGPT in Code Generation", Ouyang,
Zhang, Harman, Wang; ACM Transactions on Software Engineering and Methodology, volume 34, issue 2,
page 1-28; published online 22 Jan 2025, print 28 Feb 2025; publisher ACM. arXiv v1 5 Aug 2023,
v2 17 Oct 2024, journal-ref field points to the DOI. The ACM article number is not in the Crossref
record and the ACM DL page could not be opened, so it is not given here.

```bibtex
@article{ouyang2024nondeterminism,
  title         = {An Empirical Study of the Non-determinism of {ChatGPT} in Code Generation},
  author        = {Ouyang, Shuyin and Zhang, Jie M. and Harman, Mark and Wang, Meng},
  journal       = {ACM Transactions on Software Engineering and Methodology},
  volume        = {34},
  number        = {2},
  pages         = {1--28},
  year          = {2025},
  month         = feb,
  doi           = {10.1145/3697010},
  eprint        = {2308.02828},
  archivePrefix = {arXiv},
  primaryClass  = {cs.SE},
  url           = {https://doi.org/10.1145/3697010},
  note          = {[V-SUB] 2026-10-07 Crossref record for the DOI (online 22 Jan 2025, issue Feb 2025) and arXiv abstract page; ACM article number not confirmed (dl.acm.org returned 403)}
}
```

## 10. he2025defeating -- VERIFIED (DOI added)

Opened: https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ ;
https://api.crossref.org/works/10.64434/tml.20250910

Found, as printed: title "Defeating Nondeterminism in LLM Inference"; author line "Horace He in
collaboration with others at Thinking Machines"; date "Sep 10, 2025"; series "Connectionism". The
page's own suggested citation is `author = {Horace He and Thinking Machines Lab}`, `journal =
{Thinking Machines Lab: Connectionism}`, `doi = {10.64434/tml.20250910}`; Crossref resolves that DOI
(type report, issued 2025-09-10, publisher "Thinking Machines Lab: Connectionism"). The existing
author and date fields match; DOI added.

```bibtex
@misc{he2025defeating,
  title        = {Defeating Nondeterminism in {LLM} Inference},
  author       = {He, Horace and {Thinking Machines Lab}},
  year         = {2025},
  month        = sep,
  howpublished = {Thinking Machines Lab: Connectionism (blog)},
  doi          = {10.64434/tml.20250910},
  url          = {https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/},
  note         = {[V-SUB] 2026-10-07 blog page (author line ``Horace He in collaboration with others at Thinking Machines'', Sep 10, 2025) and Crossref record of the DOI}
}
```

## 11. bowyer2025clt -- CORRECTED (pages added)

Opened: https://proceedings.mlr.press/v267/bowyer25a.html ; https://arxiv.org/abs/2503.01747

Found: PMLR 267:81143-81184, 2025; editors Singh, Fazel, Hsu, Lacoste-Julien, Berkenkamp, Maharaj,
Wagstaff, Zhu. arXiv v1 3 Mar 2025, v3 28 May 2025, comments "42 pages, 39 figures. ICML 2025
Spotlight Position Paper", cs.AI. Title and authors identical.

```bibtex
@inproceedings{bowyer2025clt,
  title         = {Position: Don't Use the {CLT} in {LLM} Evals With Fewer Than a Few Hundred Datapoints},
  author        = {Bowyer, Sam and Aitchison, Laurence and Ivanova, Desi R.},
  booktitle     = {Proceedings of the 42nd International Conference on Machine Learning},
  series        = {Proceedings of Machine Learning Research},
  volume        = {267},
  pages         = {81143--81184},
  publisher     = {PMLR},
  year          = {2025},
  eprint        = {2503.01747},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  url           = {https://proceedings.mlr.press/v267/bowyer25a.html},
  note          = {[V-SUB] 2026-10-07 PMLR v267 page (bowyer25a) and arXiv abstract page; ICML 2025 spotlight position paper}
}
```

## 12. mann1947test -- VERIFIED

Opened: https://api.crossref.org/works/10.1214/aoms/1177730491 ;
https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-18/issue-1/On-a-Test-of-Whether-one-of-Two-Random-Variables/10.1214/aoms/1177730491.full

Found: Mann, H. B.; Whitney, D. R.; The Annals of Mathematical Statistics 18(1):50-60, March 1947;
publisher Institute of Mathematical Statistics. All fields confirmed.

```bibtex
@article{mann1947test,
  title   = {On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other},
  author  = {Mann, H. B. and Whitney, D. R.},
  journal = {The Annals of Mathematical Statistics},
  volume  = {18},
  number  = {1},
  pages   = {50--60},
  year    = {1947},
  month   = mar,
  doi     = {10.1214/aoms/1177730491},
  url     = {https://doi.org/10.1214/aoms/1177730491},
  note    = {[V-SUB] 2026-10-07 Crossref record and Project Euclid landing page}
}
```

## 13. mcgraw1992cl -- VERIFIED

Opened: https://api.crossref.org/works/10.1037/0033-2909.111.2.361

Found: "A common language effect size statistic." McGraw, Kenneth O.; Wong, S. P.; Psychological
Bulletin 111(2):361-365, 1992; publisher American Psychological Association. All fields confirmed.

```bibtex
@article{mcgraw1992cl,
  title   = {A Common Language Effect Size Statistic},
  author  = {McGraw, Kenneth O. and Wong, S. P.},
  journal = {Psychological Bulletin},
  volume  = {111},
  number  = {2},
  pages   = {361--365},
  year    = {1992},
  doi     = {10.1037/0033-2909.111.2.361},
  url     = {https://doi.org/10.1037/0033-2909.111.2.361},
  note    = {[V-SUB] 2026-10-07 Crossref record for the DOI}
}
```

## 14. efron1979bootstrap -- VERIFIED

Opened: https://api.crossref.org/works/10.1214/aos/1176344552 (no page field in the record) ;
https://projecteuclid.org/journals/annals-of-statistics/volume-7/issue-1/Bootstrap-Methods-Another-Look-at-the-Jackknife/10.1214/aos/1176344552.full

Found: B. Efron, "Bootstrap Methods: Another Look at the Jackknife", The Annals of Statistics
7(1):1-26, January 1979. All fields confirmed.

```bibtex
@article{efron1979bootstrap,
  title   = {Bootstrap Methods: Another Look at the Jackknife},
  author  = {Efron, B.},
  journal = {The Annals of Statistics},
  volume  = {7},
  number  = {1},
  pages   = {1--26},
  year    = {1979},
  month   = jan,
  doi     = {10.1214/aos/1176344552},
  url     = {https://doi.org/10.1214/aos/1176344552},
  note    = {[V-SUB] 2026-10-07 Project Euclid landing page (pages) and Crossref record}
}
```

## 15. welch1947 -- CORRECTED (issue formatting)

Opened: https://api.crossref.org/works/10.1093/biomet/34.1-2.28 ;
https://doi.org/10.1093/biomet/34.1-2.28 -> https://academic.oup.com/biomet/article-lookup/doi/10.1093/biomet/34.1-2.28

Found: Welch, B. L.; Biometrika, Volume 34, Issue 1-2, January 1947, Pages 28-35; OUP. Title as
printed by the publisher (title case): "The Generalization of 'Student's' Problem When Several
Different Population Variances Are Involved". The only change is `number = {1/2}` -> `{1--2}`,
matching the publisher's "Issue 1-2"; everything else confirmed.

```bibtex
@article{welch1947,
  title   = {The Generalization of `Student's' Problem when Several Different Population Variances are Involved},
  author  = {Welch, B. L.},
  journal = {Biometrika},
  volume  = {34},
  number  = {1--2},
  pages   = {28--35},
  year    = {1947},
  month   = jan,
  doi     = {10.1093/biomet/34.1-2.28},
  url     = {https://doi.org/10.1093/biomet/34.1-2.28},
  note    = {[V-SUB] 2026-10-07 Crossref record and OUP landing page; only if Welch p-values are reported}
}
```

## 16. chen2016xgboost -- VERIFIED

Opened: https://api.crossref.org/works/10.1145/2939672.2939785

Found: Chen, Tianqi; Guestrin, Carlos; "XGBoost: A Scalable Tree Boosting System"; Proceedings of
the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining; KDD '16, San
Francisco, California, USA; pages 785-794; 2016; ACM. All fields confirmed; publisher and address
added.

```bibtex
@inproceedings{chen2016xgboost,
  title     = {{XGBoost}: A Scalable Tree Boosting System},
  author    = {Chen, Tianqi and Guestrin, Carlos},
  booktitle = {Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
  series    = {KDD '16},
  pages     = {785--794},
  publisher = {ACM},
  address   = {San Francisco, California, USA},
  year      = {2016},
  doi       = {10.1145/2939672.2939785},
  url       = {https://doi.org/10.1145/2939672.2939785},
  note      = {[V-SUB] 2026-10-07 Crossref record for the DOI}
}
```

## 17. shwartzziv2022tabular -- VERIFIED

Opened: https://api.crossref.org/works/10.1016/j.inffus.2021.11.011

Found: Shwartz-Ziv, Ravid; Armon, Amitai; "Tabular data: Deep learning is not all you need";
Information Fusion, volume 81, pages 84-90, May 2022; Elsevier. (Crossref lists issue "C", an
Elsevier placeholder; no issue number is used.) All fields confirmed; month added.

```bibtex
@article{shwartzziv2022tabular,
  title   = {Tabular data: Deep learning is not all you need},
  author  = {Shwartz-Ziv, Ravid and Armon, Amitai},
  journal = {Information Fusion},
  volume  = {81},
  pages   = {84--90},
  year    = {2022},
  month   = may,
  doi     = {10.1016/j.inffus.2021.11.011},
  url     = {https://doi.org/10.1016/j.inffus.2021.11.011},
  note    = {[V-SUB] 2026-10-07 Crossref record for the DOI}
}
```

## 18. rubachev2024tabred -- CORRECTED (conference version: ICLR 2025)

Opened: https://arxiv.org/abs/2406.19380 ;
https://proceedings.iclr.cc/paper_files/paper/2025/hash/571799482291411607c54984153190b0-Abstract-Conference.html
and its BibTeX (https://proceedings.iclr.cc/paper_files/paper/2789-/bibtex) ;
https://research.yandex.com/blog/papers-accepted-to-iclr-and-naacl-2025 (authors' lab, supporting) ;
https://openreview.net/forum?id=L14sqcrUC3 (blocked by a browser check)

Found: arXiv v1 27 Jun 2024 ... v4 24 Oct 2024, cs.LG. ICLR 2025 proceedings BibTeX: booktitle
International Conference on Learning Representations, volume 2025, pages 35166--35202, editors
Y. Yue, A. Garg, N. Peng, F. Sha, R. Yu. Title and four authors identical. Entry type changed from
@misc to @inproceedings and year from 2024 to 2025 (key kept).

```bibtex
@inproceedings{rubachev2024tabred,
  title         = {{TabReD}: Analyzing Pitfalls and Filling the Gaps in Tabular Deep Learning Benchmarks},
  author        = {Rubachev, Ivan and Kartashev, Nikolay and Gorishniy, Yury and Babenko, Artem},
  booktitle     = {International Conference on Learning Representations (ICLR)},
  pages         = {35166--35202},
  year          = {2025},
  eprint        = {2406.19380},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  url           = {https://proceedings.iclr.cc/paper_files/paper/2025/hash/571799482291411607c54984153190b0-Abstract-Conference.html},
  note          = {[V-SUB] 2026-10-07 ICLR 2025 proceedings page and BibTeX (OpenReview L14sqcrUC3), arXiv abstract page (v4 24 Oct 2024); time-based splits}
}
```

---

## arXiv id check for ALL entries (46 `eprint` fields)

Method: each https://arxiv.org/abs/<id> page was opened on 2026-10-07 and its `citation_title`
meta tag compared with the bib title. All 46 ids resolve to the cited paper. Four show wording or
capitalisation differences, flagged in the last column.

| key | eprint | title on arXiv | match |
|---|---|---|---|
| arino2026identicalruns | 2609.33812 | Identical Runs, Different Results: Benchmarking AI Coding Agents on Open-Weight Models | yes |
| ferreira2026autoresearch | 2603.24647 | Can LLMs Beat Classical Hyperparameter Optimization Algorithms? A Study on autoresearch | yes |
| rodrigues2026llmhpo | 2606.21641 | When Is an LLM Worth It for Hyperparameter Optimization? A Budget-Matched Study on Tabular Data Finds the Warm-Start Is a Default Configuration, Not the Model | yes |
| zhang2023llmhpo | 2312.04528 | Using Large Language Models for Hyperparameter Optimization | yes |
| liu2024llambo | 2402.03921 | Large Language Models to Enhance Bayesian Optimization | yes |
| liu2024agenthpo | 2402.01881 | Large Language Model Agent for Hyper-Parameter Optimization | yes |
| huang2024mlagentbench | 2310.03302 | MLAgentBench: Evaluating Language Agents on Machine Learning Experimentation | yes |
| guo2024dsagent | 2402.17453 | DS-Agent: Automated Data Science by Empowering Large Language Models with Case-Based Reasoning | yes |
| jiang2025aide | 2502.13138 | AIDE: AI-Driven Exploration in the Space of Code | yes |
| chan2024mlebench | 2410.07095 | MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering | yes |
| wijk2025rebench | 2411.15114 | RE-Bench: Evaluating frontier AI R&D capabilities of language model agents against human experts | yes (capitalisation differs only) |
| jing2025dsbench | 2409.07703 | DSBench: How Far Are Data Science Agents from Becoming Data Science Experts? | yes |
| li2024autokaggle | 2410.20424 | AutoKaggle: A Multi-Agent Framework for Autonomous Data Science Competitions | yes |
| grosnit2024agentk | 2411.03562 | Kolb-Based Experiential Learning for Generalist Agents with Human-Level Kaggle Data Science Performance | yes |
| nam2025mlestar | 2506.15692 | MLE-STAR: Machine Learning Engineering Agent via Search and Targeted Refinement | yes |
| rahman2026dsagentbench | 2608.10366 | DSAgentBench: Can Agents Automate End-to-End Data-Science Workflows in Real Computer Environments? | yes |
| moukpe2026deltaml | 2608.19653 | DeltaML-Bench: Evaluating Machine Learning Agents on Real-World Research Repositories | yes |
| ouyang2024nondeterminism | 2308.02828 | An Empirical Study of the Non-determinism of ChatGPT in Code Generation | yes |
| atil2025nondeterminism | 2408.04667 | Non-Determinism of "Deterministic" LLM Settings | yes |
| yao2024taubench | 2406.12045 | $\tau$-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains | yes |
| rabanser2026reliability | 2602.16666 | Towards a Science of AI Agent Reliability | yes |
| bjarnason2026randomness | 2602.07150 | On Randomness in Agentic Evals | yes |
| mehta2026disagree | 2602.11619 | When Agents Disagree With Themselves: Behavioral Consistency as an Uncertainty Signal for LLM Agents | yes |
| madaan2024variance | 2406.10229 | Quantifying Variance in Evaluation Benchmarks | yes |
| wang2025noises | 2512.21326 | Measuring all the noises of LLM Evals | yes |
| bowyer2025clt | 2503.01747 | Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints | yes |
| hariri2026dontpassk | 2510.04265 | Don't Pass@k: A Bayesian Framework for Large Language Model Evaluation | yes |
| miller2024errorbars | 2411.00640 | Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations | yes |
| kapoor2024agents | 2407.01502 | AI Agents That Matter | yes |
| henderson2018deep | 1709.06560 | Deep Reinforcement Learning that Matters | yes (capitalisation differs only) |
| colas2018seeds | 1806.08295 | How Many Random Seeds? Statistical Power Analysis in Deep Reinforcement Learning Experiments | yes |
| agarwal2021precipice | 2108.13264 | Deep Reinforcement Learning at the Edge of the Statistical Precipice | yes |
| bouthillier2021variance | 2103.03098 | Accounting for Variance in Machine Learning Benchmarks | yes |
| dodge2020finetuning | 2002.06305 | Fine-Tuning Pretrained Language Models: Weight Initializations, Data Orders, and Early Stopping | yes |
| chen2021codex | 2107.03374 | Evaluating Large Language Models Trained on Code | yes |
| brown2024monkeys | 2407.21787 | Large Language Monkeys: Scaling Inference Compute with Repeated Sampling | yes |
| dwork2015generalization | 1506.02629 | Generalization in Adaptive Data Analysis and Holdout Reuse | yes |
| lewis2026same | 2608.26218 | Same Model, Different Harness: Different Coding-Agent Results | yes |
| fan2026harness | 2609.20804 | An Empirical Study of Harness Design for Coding Agents | yes |
| zhao2026specbench | 2605.21384 | SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents | yes |
| chen2026publicscore | 2604.20200 | Chasing the Public Score: User Pressure and Evaluation Exploitation in Coding Agent Workflows | yes |
| zhu2025abc | 2507.02825 | Establishing Best Practices **for** Building Rigorous Agentic Benchmarks | yes, but the bib says "Best Practices **in** Building" -- arXiv (v5, 7 Aug 2025) prints "for"; check the NeurIPS 2025 D&B title before the camera-ready |
| grinsztajn2022tabular | 2207.08815 | Why do tree-based models still outperform deep learning on tabular data? | yes, but the bib title has "typical tabular data" (the NeurIPS 2022 title per the entry's own note); the arXiv title omits "typical" |
| rubachev2024tabred | 2406.19380 | TabReD: Analyzing Pitfalls and Filling the Gaps in Tabular Deep Learning Benchmarks | yes |
| gardner2023tableshift | 2312.07577 | Benchmarking Distribution Shift in Tabular Data with TableShift | yes |
| cai2025temporal | 2502.20260 | Understanding the Limits of Deep Tabular Methods with Temporal Shift | yes |

No id points to a different paper.

---

## Summary

| status | count | keys |
|---|---|---|
| VERIFIED | 8 | arino2026identicalruns, pafka2015benchmml, he2025defeating, mann1947test, mcgraw1992cl, efron1979bootstrap, chen2016xgboost, shwartzziv2022tabular |
| CORRECTED | 10 | karpathy2026autoresearch (first commit 6 Mar 2026 UTC), openai2026codex (split: release 0.160.0 of 1 Oct 2026 + config reference), openai2026gpt6 (official URLs, prices, effort levels, dates), zhang2023llmhpo (NeurIPS 2023 FMDM workshop), huang2024mlagentbench (PMLR 235:20271-20309), jing2025dsbench (ICLR 2025 pp. 32597-32649), ouyang2024nondeterminism (TOSEM 34(2):1-28), bowyer2025clt (PMLR 267:81143-81184), welch1947 (issue 1-2), rubachev2024tabred (ICLR 2025 pp. 35166-35202) |
| COULD NOT OPEN | 0 | -- |

Pages that could not be opened (alternatives were used in each case): openreview.net forum pages
(browser check), dl.acm.org/doi/10.1145/3697010 (403), openai.com announcement pages (403),
x.com (Karpathy's announcement). Two non-flagged entries deserve a look before the camera-ready:
zhu2025abc title wording ("for" vs "in") and grinsztajn2022tabular ("typical" present only in the
NeurIPS title).
