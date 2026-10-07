# 05. Related work: themes, papers, positioning

## Ground rules

1. The starting point was `harness_benchmark/paper/refs.bib`, `harness_benchmark/docs/literature/
   {deep-research-2026-09-18.md, verification.md}` and the related-work section of the companion
   paper (`identical-runs-different-results/paper/identical-runs-different-results.md`). From
   these only **bibliographic entries and the themes** were taken. **No result, number, table,
   figure or finding of the companion paper or of `harness_benchmark` is used anywhere in this
   paper.**
2. Every entry in `references.bib` carries either a verified status (opened at the primary source,
   either in `verification.md` on 2026-09-18 or by this plan on 2026-10-07) or a `TO VERIFY` note.
   Open each `TO VERIFY` entry before citing; drop what cannot be opened.
3. Cite what the paper actually leans on. Target 35 to 50 references.

## The companion paper (Ariño de la Rubia and Pafka, arXiv 2609.33812)

Authors' decision (2026-10-07): at most one brief, high-level mention in related work, and at
most one clause in the introduction; no emphasis. For example, in related work:

> A companion study by the same authors (Ariño de la Rubia and Pafka, 2026) also uses repeated
> runs of coding agents on an XGBoost tuning task, with open-weight models and several agent
> harnesses. The present paper holds the agent fixed and varies the LLM; its claims rest only on
> the 60 runs reported here.

Do not describe its findings, do not quote its numbers, do not compare magnitudes with it, do
not reuse its figures or tables, and do not return to it in the discussion.

## Themes, with the papers and where they are cited

### A. Agents that do machine-learning engineering (Related work 2.1; Introduction)

| Key | What it is | Use in the paper |
|---|---|---|
| `pafka2026autoresearch` | The authors' previous project: an agent researches, engineers features and tunes XGBoost on the same airline data; single runs | first paragraph of the introduction; methods (lineage of the task) |
| `karpathy2026autoresearch` | Karpathy's autoresearch (March 2026): an agent edits a training script in a loop under a fixed 5-minute budget per experiment, keeps or reverts, guided by a `program.md`; nanochat on one GPU | origin of the loop and of `program.md`; methods |
| `ferreira2026autoresearch` | Uses autoresearch as a testbed to compare LLM agents with classical HPO under a fixed budget | closest methodological relative; note they ask a different question (agents vs classical search) |
| `rodrigues2026llmhpo` | Budget-matched multi-seed study of an LLM advisor for HPO on tabular data | the multi-seed protocol is the right instinct; different question |
| `zhang2023llmhpo`, `liu2024llambo`, `liu2024agenthpo` | LLMs proposing hyperparameters, LLMs inside Bayesian optimisation, an LLM agent for HPO | one sentence: LLMs as tuners is an active line; our agent tunes by editing code and engineering features |
| `huang2024mlagentbench`, `guo2024dsagent`, `jiang2025aide`, `chan2024mlebench`, `wijk2025rebench`, `jing2025dsbench`, `li2024autokaggle`, `grosnit2024agentk`, `nam2025mlestar`, `rahman2026dsagentbench`, `moukpe2026deltaml` | Benchmarks and agents for ML engineering and data science | one paragraph: breadth of tasks there, depth of repetition here; MLE-bench's README asks for at least 3 seeds because agents are high-variance; RE-Bench aggregates attempts as best-of-k; DeltaML-Bench compares resource allocations |

### B. Variation between identical runs of LLMs and agents (Related work 2.2; Introduction)

| Key | What it is | Use |
|---|---|---|
| `ouyang2024nondeterminism` | Non-determinism of ChatGPT code generation, even at temperature 0 | nondeterminism of a single LLM call |
| `atil2025nondeterminism` | "Deterministic" settings still vary across identical inputs | same |
| `he2025defeating` | Thinking Machines: why inference endpoints are nondeterministic (batch-size-dependent kernels), batch-invariant kernels as a fix | the source of randomness at the lowest level; our agent runs compound it over hundreds of calls |
| `yao2024taubench` | pass^k: consistency of an agent over repeated trials | agent reliability as a metric |
| `rabanser2026reliability` | Twelve reliability metrics; a single success rate hides consistency | same |
| `bjarnason2026randomness` | Ten runs of six coding-agent configurations on SWE-bench Verified; single-run pass@1 moves by points; power analysis for the number of runs | the closest study on coding agents; theirs is a pass rate over many tasks, ours a continuous score on one task with 20 identical runs |
| `mehta2026disagree` | Behavioural variance across identical agent runs as an uncertainty signal | agent runs diverge in their action sequences |
| `madaan2024variance`, `wang2025noises`, `bowyer2025clt`, `hariri2026dontpassk`, `miller2024errorbars` | Variance and uncertainty in LLM evaluation; error bars; small-sample caveats; Bayesian alternatives to pass@k | statistics of evaluation; justify intervals and bootstrap with n = 20; cite Bowyer for the warning that CLT intervals on few points are optimistic (we use t and bootstrap, and 20 runs, not hundreds) |
| `henderson2018deep`, `colas2018seeds`, `agarwal2021precipice`, `bouthillier2021variance`, `dodge2020finetuning` | Seed variance and few-run comparisons in deep RL and ML benchmarks; how many seeds; interval estimates | the older lesson; our runs are the agent analogue of seeds |

### C. Comparing noisy systems and selecting among attempts (Related work 2.3; Methods 3.7; Discussion)

| Key | What it is | Use |
|---|---|---|
| `mann1947test`, `mcgraw1992cl`, `vargha2000a` | Mann–Whitney; the common-language effect size; the A measure with ties half | the head-to-head statistic is exactly Vargha–Delaney A |
| `efron1979bootstrap` | the bootstrap | intervals of A |
| `welch1947` (optional) | Welch's t | if p-values are reported |
| `hanley1982meaning`, `delong1988comparing` | AUC standard error; paired AUC comparison | the ~0.002 sampling error of eval and holdout AUC; eval and holdout paired |
| `miller2024errorbars` | power and sample-size formulas for evals | the 16 sd²/gap² approximation |
| `chen2021codex`, `brown2024monkeys`, `wijk2025rebench` | repeated sampling raises the best result; best-of-k | the "run several times and pick" advice |
| `cawley2010overfitting`, `dwork2015reusable`, `dwork2015generalization`, `roelofs2019meta` | selection bias when choosing on the evaluation set; reusable holdout; little adaptive overfitting in Kaggle | why a third untouched set is needed after selecting the best of k on the eval set; why the small eval–holdout gap here is plausible |

### D. Agents as deployed systems; rule-following (Related work 2.4; Methods 3.6)

| Key | What it is | Use |
|---|---|---|
| `lewis2026same`, `fan2026harness`, `pan2026harnesstax` | harness effects depend on the model; cost and success by harness | our design holds the harness fixed and varies the LLM; what varies between our runs is the deployed agent–LLM–service system |
| `arino2026identicalruns` | the companion paper | design-level citation only (see above) |
| `kapoor2024agents` | evaluate agents on cost and accuracy; run several times | one sentence |
| `metr2025o3`, `zhao2026specbench`, `chen2026publicscore`, `moukpe2026deltaml`, `zhu2025abc` | reward hacking, public-score exploitation, benchmark rigor | motivation for the integrity checks (holdout out of reach, row-by-row scoring, leak check of the session log); we found no violation |

### E. Tabular learning and temporal shift (Related work 2.5; Methods 3.1; Results 4.5)

| Key | What it is | Use |
|---|---|---|
| `chen2016xgboost` | XGBoost | the model |
| `grinsztajn2022tabular`, `shwartzziv2022tabular` | tree ensembles still win on tabular data | why XGBoost is the right object |
| `rubachev2024tabred`, `gardner2023tableshift`, `cai2025temporal` | time-based splits change rankings; temporal shift in tabular benchmarks | why train on 2005 and evaluate on 2006; why the day-of-month category overfits the training year |
| `dataexpo2009`, `pafka2015benchmml` (TO VERIFY) | the airline data and the authors' long-standing benchmark slices | data provenance |

## Positioning paragraph (to close Related work)

> Run-to-run variation of LLM agents, the need for repeated runs and power analysis, best-of-k
> selection, and agents' sensitivity to their harness are each documented. This paper adds a
> measurement a practising data scientist can use: on one realistic tabular task, with one
> agent and three frontier LLMs at a fixed effort, 20 identical and independently audited runs
> each, how wide the distribution of the delivered model's holdout AUC is, how it compares with
> the gaps between LLMs, how often a single run of each ranks two LLMs wrongly, how the variation
> arises over the hour, and which modelling decisions account for part of it. The building block
> and the orchestrator make the same measurement repeatable for other agents, LLMs and prompts.

## Still to do for the related-work section

- Done 2026-10-07: every flagged entry opened at its primary source (`verification/bib-verification.md`): 8 confirmed, 10 corrected, none unopenable; all 46 arXiv ids resolve to the cited titles. The official OpenAI model pages and the Codex configuration reference are now cited (`openai2026gpt6`, `openai2026codex`, `openai2026codexconfig`).
- Done 2026-10-07: the two title wordings checked against the proceedings. `zhu2025abc` uses "in Building" in the NeurIPS 2025 proceedings, as the bib does (arXiv says "for"); its author list was wrong (25 of 26 authors, Narayanan missing, Kellermann misplaced) and is corrected. `grinsztajn2022tabular` cites the NeurIPS version, whose title has "typical", as the bib does.
- Decide whether to cite one or two sources on reasoning-effort / test-time-compute settings.
- Search log of this plan (2026-10-07, WebSearch standard mode): Karpathy autoresearch; variance
  and nondeterminism in agent evals; DS/AutoML agent benchmarks; LLM HPO; Bowyer; Madaan; Thinking
  Machines; Colas; Grinsztajn; temporal shift benchmarks; Codex CLI reasoning effort; Kaggle
  agents; repeated sampling; probability of superiority; GPT-6 model names. arXiv abstract pages
  opened for: 2602.11619, 2608.13867 (not used), 2604.13413 (not used), 2512.21326, 2408.04667,
  2308.02828, 2510.04265, 2310.03302, 2502.13138, 2402.03921, 2409.07703, 2411.03562, 2506.15692,
  2406.19380, 2402.17453, 2407.21787, 2402.01881, 2502.20260, 2503.01747, 2406.10229, 2608.10366,
  2410.20424, 2312.07577; github.com/karpathy/autoresearch; szilard.github.io/xgboost-autoresearch.
