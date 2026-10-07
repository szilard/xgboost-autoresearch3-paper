# 01. Main points: thesis, claims, numbers

## Working title

Keep the blog title for arXiv, it is accurate and already public:

> **One Run Is Not Enough: How Much AI Agent Results Vary in Data Science, an XGBoost Optimization Study**

Alternatives if the authors want a more conventional arXiv title (decide in `08-decisions-for-authors.md`):
- "One Run Is Not Enough: Run-to-Run Variation of an AI Coding Agent Tuning XGBoost, Across Three LLMs"
- "How Much Do AI Agent Results Vary? Twenty Identical Runs per LLM on an XGBoost Tuning Task"

Authors: Szilard Pafka (Epoch) and Eduardo Ariño de la Rubia (Central European University), the
order and affiliations as on the blog post and the companion paper, with emails under the
affiliations (confirmed by the authors, 2026-10-07).

## Thesis (one paragraph, the paper's spine)

An AI coding agent (OpenAI Codex, on a ChatGPT subscription) was given one hour, identical
instructions and an isolated container to improve a starter XGBoost model on a flight-delay task,
twenty times with each of three OpenAI LLMs (gpt-6-luna, gpt-6-sol, gpt-6-astra; Luna, Sol, Astra),
all at the "max" reasoning effort. Every one of the 60 runs improved the starter model on a holdout
set the agent never saw, and on average the three LLMs rank clearly. But the run-to-run spread
within an LLM is of the same order as the differences between LLMs, so one run is not enough,
either to judge how well a setup performs or to compare LLMs. The paper measures that spread, shows
how it builds up over the hour, traces part of the between-LLM gap to one modelling decision (how
the calendar is handled), and draws two practical consequences: compare setups on distributions
from repeated runs, and when the goal is a good model, run several times and pick the best on data
the agent has not seen, then confirm on untouched data.

## Contributions to state in the introduction

1. **A minimal, standardized, open building block for one autonomous run**
   (`xgboost-autoresearch-minimal3`: one editable file, a harness that keeps the clock, times and
   kills experiments, saves an artifact per commit and scores the evaluation set row by row; a
   holdout set and human-only scripts out of the agent's reach) and **an orchestrator that runs it
   repeatedly without human steering** (`xgboost-autoresearch-minimal3-runs`: fresh Docker
   container per run, pinned code, identical turns, automatic integrity and protocol checks,
   holdout scoring, archived session logs). Both are open source so others can test their own
   agents, LLMs and setups with more than one run each.
2. **Sixty fully automated, independently audited runs**: three frontier LLMs x 20 runs, same
   agent, same prompt, same image, same machine type, no run excluded.
3. **Measurements of run-to-run variation** on a continuous outcome (holdout AUC): per-LLM
   distributions, head-to-head single-run win probabilities, and the time course of the holdout
   AUC within the hour.
4. **A partial mechanism**: which modelling choices separate the LLMs and the runs (calendar
   handling: day-of-month as a category versus numeric or holiday features), and the role of luck
   (order and follow-up of ideas).
5. **Practical guidance**: how to compare agents, LLMs, prompts or setups (repeated runs,
   distributions), and how to get a good model (run several times, pick on unseen data, confirm
   on untouched data).

## The claims, each with its verified numbers

All numbers below were recomputed on 2026-10-07 from `run-multi/*/holdout_auc.tsv` and the
per-run files (script and output in `03-data-and-analysis.md`). "Holdout AUC" is the holdout AUC
of each run's final model, i.e. the kept model with the highest evaluation AUC (on a tie, the last
kept commit). Starter model: eval AUC 0.6743, holdout AUC 0.6725.

### Claim 1. Every run improves the starter model

- 60 of 60 runs have holdout AUC above 0.6725. The weakest run is luna6_n20-11 at 0.6773 (+0.0048).
- Mean improvement over the starter: Luna +0.0081, Sol +0.0117, Astra +0.0141 (blog: 0.008, 0.012, 0.014).

### Claim 2. On average the LLMs rank clearly: Astra > Sol > Luna

| LLM | n | mean | sd | 95% CI of the mean (t) | median | min | max |
|---|---|---|---|---|---|---|---|
| gpt-6-astra | 20 | 0.6866 | 0.0022 | 0.6855 to 0.6876 | 0.6871 | 0.6815 | 0.6906 |
| gpt-6-sol | 20 | 0.6842 | 0.0018 | 0.6833 to 0.6850 | 0.6844 | 0.6803 | 0.6871 |
| gpt-6-luna | 20 | 0.6806 | 0.0019 | 0.6798 to 0.6815 | 0.6800 | 0.6773 | 0.6844 |

- The three confidence intervals do not overlap. Differences of means: Astra − Sol +0.0024,
  Sol − Luna +0.0035, Astra − Luna +0.0059 (the blog's "0.006 between the averages of the best and
  the worst LLM").
- Supporting tests (optional in the paper, keep in the appendix if used): Welch t-test p = 6e-4
  (Astra vs Sol), 6e-7 (Sol vs Luna), 4e-11 (Astra vs Luna); Mann-Whitney p = 1.2e-3, 9e-6, 2.5e-7;
  one-way ANOVA p = 1.6e-12; Kruskal-Wallis p = 9.4e-9.
- Unrounded means: 0.68065 (Luna), 0.68418 (Sol), 0.68656 (Astra).

### Claim 3. Within an LLM, runs vary a lot, and the ranges overlap

- 10th and 90th percentiles (nearest run): Luna 0.6789 / 0.6831; Sol 0.6821 / 0.6864; Astra 0.6845 / 0.6888.
- Full range (best − worst): Luna 0.0071, Sol 0.0068, Astra 0.0091 (blog: "0.007 to 0.009").
- Range as a share of the LLM's mean improvement: Luna 0.87, Sol 0.58, Astra 0.65 (blog: "more
  than half of its average improvement"). Each range is also larger than the 0.0059 between the
  best and the worst LLM's means.
- Overlap: Luna's best run (0.6844) beats 10 of Sol's 20 runs and 2 of Astra's 20 (blog: "half of
  Sol's runs and the two worst runs of Astra"); Sol's best run (0.6871) beats 10 of Astra's 20
  (blog: "half of Astra's runs").

### Claim 4. One run of each LLM ranks two LLMs wrong surprisingly often

Probability that a random run of the better LLM (by mean) beats a random run of the other, over all
20 x 20 pairs, ties (at 4 decimals) counted half; 95% percentile bootstrap over runs, 10,000
resamples, seed 1 (as `tools/pairwise_win_prob.py`):

| pair | P(better wins) | 95% bootstrap interval |
|---|---|---|
| Astra vs Luna | 0.978 (98%) | 0.927 to 1.000 |
| Sol vs Luna | 0.911 (91%) | 0.810 to 0.983 |
| Astra vs Sol | 0.801 (80%) | 0.656 to 0.925 |

So Sol still wins one pairing in five against Astra, although the means differ by 3.5 standard
errors of the difference.

### Claim 5. The variation builds up over the hour in a recognisable way

From the per-run holdout AUC paths (kept model over time since the clock started):

- Most runs make the same first move: shallower trees (depth 3 or 4 instead of 6, often more
  trees at a lower learning rate), lifting holdout AUC from 0.6725 to about 0.678. Adding trees at
  the starter's learning rate lowers eval AUC on this data (a model that fits 2005 more closely
  does worse on 2006). Source: the group `results_summary.md` "What worked" notes and the per-run
  `results.tsv` descriptions; quantify with the feature/parameter audit (see `03`).
- Median time to the first holdout gain (> +0.0005): Astra 2.4 min, Sol 2.9 min, Luna 5.4 min.
- Median holdout AUC of the kept model at 15 / 30 / 45 / 60 min:
  Astra 0.6819 / 0.6836 / 0.6849 / 0.6871; Sol 0.6826 / 0.6833 / 0.6837 / 0.6844;
  Luna 0.6784 / 0.6790 / 0.6797 / 0.6800. (Sol and Astra "neck and neck at the half hour"; most of
  the Astra–Sol gap opens in the second half hour; Luna's median sits at 0.678 to 0.680 from
  15 minutes on.)
- Experiments per run (rows of `results.tsv`, baseline included, kept or discarded): Luna 30.1
  (24 to 38), Sol 45.1 (29 to 70), Astra 47.1 (36 to 62) (blog: 30, 45, 47). Kept commits per run:
  Luna 8.7, Sol 13.0, Astra 19.2 on average.
- Share of the hour the agent spends outside XGBoost runs ("AI share" of the harness report):
  Luna 67.7%, Sol 53.6%, Astra 71.5%.
- Longest plateau without a kept change, median per run: Luna 19.6 min, Sol 14.2 min, Astra
  10.7 min; runs with a plateau of 20 minutes or more: Luna 9, Sol 3, Astra 2 (blog: "others get
  stuck on a plateau for 20 minutes or more").
- Steps down on the holdout set (a kept eval gain that does not carry over), mean per run: Luna
  0.90, Sol 1.55, Astra 2.25. Runs whose final model scores below their best kept model on the
  holdout set: Luna 3, Sol 6, Astra 4.

### Claim 6. Part of the between-LLM gap comes down to the calendar

The starter treats `Month` and `DayofMonth` as categories, which together identify the date and
let the model learn particular days of 2005. From the heuristic audit of the 60 final `train.py`
files (the list assigned to `cat_cols`, plus text matches; see `03` for the script and the manual
verification still owed):

| LLM | final models that dropped `DayofMonth` as a category | with holiday features | with a day-of-year-like numeric feature | mean holdout, dropped vs kept |
|---|---|---|---|---|
| Astra | 19 of 20 | 15 | 11 | 0.6867 vs 0.6836 (one run kept it) |
| Sol | 13 of 20 | 3 | 16 | 0.6852 vs 0.6823 (+0.0028) |
| Luna | 4 of 20 (runs 9, 17, 18, 20: its three best among them) | 2 | 5 | 0.6834 vs 0.6800 (+0.0034) |

Blog wording to keep: "Astra dropped the day-of-month category in 19 of its 20 runs, often among
its first changes, and 15 of its 20 final models use holiday features instead ... Sol dropped it
in 13 runs, mostly in favor of the day of the year as a number, and Luna in only 4, its three best
runs among them. Within Luna's runs and within Sol's, those that dropped it score about 0.003
higher on the holdout set on average than those that kept it. But a good idea alone does not
guarantee a good result: Astra's weakest run also dropped the day-of-month category and used
holidays." (astra6_n20-4, holdout 0.6815, is to be confirmed in the audit.)

### Claim 7. Practical consequences

1. To compare agents, LLMs, prompts or any other part of a setup, one run is not enough: run
   repeatedly and look at the distribution, not a single number. (Optional quantification, post
   hoc and to be labelled as such: with the observed median SD of 0.0019, the usual approximation
   16 sd² / gap² for 80% power at 5% two-sided gives about 10 runs per arm for the Astra–Sol gap of
   0.0024, 5 for Sol–Luna, 2 for Astra–Luna; and the bootstrap intervals above show that 20 runs
   per LLM still leave the Astra–Sol win probability between 66% and 93%.)
2. If the goal is a good model, run the agent several times and pick the best run on data the agent
   has not seen; estimate the chosen model on another untouched test set. Supporting new analysis
   (best-of-k, choosing on eval AUC, reporting holdout AUC, median over draws with replacement):
   Astra 0.6870 (k=1), 0.6881 (3), 0.6886 (5), 0.6888 (10); Sol 0.6841, 0.6856, 0.6857, 0.6857;
   Luna 0.6800, 0.6820, 0.6831, 0.6844. Eval and holdout AUC rank a LLM's runs almost identically
   (Spearman 0.94 Astra, 0.91 Sol, 0.96 Luna), so selecting on eval is nearly as good as selecting
   on holdout.

### Secondary observations (supporting, not headline)

- **Eval–holdout gap** (holdout − eval of the final model): Luna −0.0018 (sd 0.0006), Sol −0.0018
  (0.0007), Astra −0.0028 (0.0005); the starter's gap is −0.0018. Selection on the eval set
  overfits it only slightly, somewhat more for Astra (more kept commits, higher eval AUC).
  Eval and holdout are disjoint halves of one balanced 100K sample of 2006, each AUC has a
  sampling error of about 0.002 (Hanley–McNeil, 25K per class), and the two are paired.
- **Integrity**: no run was excluded. The automatic checks flagged 10 runs; all flags were false
  alarms on review (false `glob`/`global` matches in luna 1, 7, 11, 15 and sol 12; a `train.csv`
  read written differently in astra 15; two artifacts from in-clock runs without their own timing
  row in astra 4 and 16; one false-positive content hit each in astra 6 and 8). Leak checks: 0
  content hits in every run after review.
- **Protocol caveats**: 10 runs. Nine kept a tie without being simpler or faster
  (luna 6, 8, 15, 18; sol 8, 19; astra 5, 8, 12); one lost 216 s of its hour to capacity retries
  (sol 16). All 60 runs are analysed alike; a sensitivity check without the caveat runs belongs in
  the appendix (`tools/pairwise_win_prob.py --no-caveat` exists).
- **For the human to judge** (reported, not excluded): astra 7 and 12 mapped carrier HP to US
  after reading BTS documentation that the two report jointly from 2006 (worth +0.0004 and
  +0.0007 on holdout when made); sol 11 and astra 12 built holiday windows from a TranStats table
  of holiday travel seasons by year. No run saw flight records, eval rows or holdout rows.
- **Operational**: every run's agent stopped the clock itself; "go" sent once per run except luna
  18 and sol 20 (twice); "keep going" only in astra 4 after a capacity error; context compactions
  in 11 of 20 Astra runs and 2 Sol runs, none disturbed the protocol; peak container memory 3.4 to
  16.5 GiB, nothing killed at the 24 GB cap.

## What the paper does not claim

- Not a general ranking of the three LLMs: one agent, one task, one dataset, one hour, one effort
  setting, runs over three days through a hosted service whose builds and load are not pinned.
- Not a statement that the agents' models beat classical tuning or a human; no such arm was run.
- Not a statement about later years: eval and holdout both come from 2006 (a 2007 check is listed
  as optional future work in `03`; nothing of the kind is borrowed from the companion paper).
- Not evidence of rule-breaking: none was found; the integrity machinery is a methods contribution.
- No cost claim. Token usage per run is reported in an appendix from the session logs, with a
  list-price projection labelled as such (the runs ran on a ChatGPT subscription).
