# 04. Figures and tables

Palette and conventions follow the runs repo's tools (Astra `#2a78d6`, Sol `#eb6834`, Luna
`#1baf7a`; rows ordered by mean holdout AUC, best on top; grey range bars; black mean and
interval). Regenerate everything as vector PDF (plus PNG for the repo README) from
`analysis/make_figures.py`; do not paste the blog PNGs into the paper (they are 150 dpi raster
with the blog's title text). Captions below are drafts.

## Figures

| # | Figure | Source / script | Status |
|---|---|---|---|
| F1 | Holdout AUC per run, beeswarm per LLM: dots per run, grey full range, ticks at the 10th and 90th percentile, black mean with 95% t-interval | `tools/plot_holdout_auc.py` (strip_plot) via `make_figures.py` | exists as `docs/holdout_auc_beeswarm.png`; regenerate as PDF |
| F2 | Head to head: P(one run of the better LLM beats one run of the other) for the three pairs, with 95% bootstrap intervals and the coin-flip line | `tools/pairwise_win_prob.py` | exists; regenerate |
| F3 | Holdout AUC path per run, all 60 runs faded, median path per LLM in bold, x = minutes since the clock started | `tools/plot_holdout_auc.py` (path_median) | exists; regenerate |
| F4 | Same, one panel per LLM, other LLMs' runs grey behind | `tools/plot_holdout_auc.py` (path_panels) | exists; regenerate; consider full-width placement |
| F5 | Eval AUC vs holdout AUC of each run's final model, one dot per run coloured by LLM, the diagonal and the starter's gap line; shows the small, stable gap and the near-monotone relation | new, `gap.py` + `make_figures.py` | new |
| F6 | Best-of-k: median (and 5th–95th band) holdout AUC of the run chosen by eval AUC among k draws, k = 1..10, one line per LLM; dashed: oracle choosing on holdout | new, `best_of_k.py` | new, optional |
| F7 | Feature audit bars: share of final models per LLM that keep `DayofMonth` as a category, use a numeric day of year, use holiday features (and tree depth ≤ 4) | new, `feature_audit.py` | new |
| F8 | (Appendix) One run in detail: eval and holdout AUC of each kept commit over the hour with the description of each keep (e.g. astra6_n20-1, 19 keeps), i.e. a cleaned `auc_history.png` | new, from `holdout_scores.tsv` + `timing/runs.tsv` | optional |
| F9 | (Appendix, optional) Experiments per run vs holdout AUC, by LLM (Spearman 0.36 to 0.45, exploratory) | new | optional |

Draft captions:

- **F1.** Holdout AUC of each run's final model (the kept model with the highest evaluation AUC),
  20 runs per LLM. Dots: runs. Grey bar: full range. Vertical ticks: 10th and 90th percentiles.
  Black dot and whiskers: mean and its 95% confidence interval. The starter model scores 0.6725.
- **F2.** Probability that a randomly chosen run of the LLM named on the right beats a randomly
  chosen run of the LLM named on the left, estimated from all 400 pairs of runs (ties counted
  half), with 95% bootstrap intervals (runs resampled within each LLM, 10,000 resamples).
- **F3.** Holdout AUC of the kept model over the hour, one thin line per run and the median over
  each LLM's runs in bold. Each step is a change the agent kept on the evaluation set; steps down
  are kept gains that did not carry over to the holdout set.
- **F4.** As F3, one panel per LLM, with the other two LLMs' runs in grey behind.
- **F5.** Evaluation AUC against holdout AUC of each run's final model. The dotted line is
  equality; the eval and holdout sets are disjoint halves of one 2006 sample, and the agent
  selected on the evaluation set.
- **F7.** How the final models handle the calendar, by LLM: share that keeps the day of the month
  as a category (as the starter does), share with a numeric day-of-year-like feature, share with
  holiday features. From a scripted audit of the 60 final `train.py` files, checked by hand.

## Tables

| # | Table | Content | Source | Status |
|---|---|---|---|---|
| T1 | Setup | task, data sizes and years, metric, starter model, budget and timeouts, agent and version, LLMs and effort, image and package versions, machine, dates, number of runs | `02-outline.md` §3, `run.md` files | to assemble |
| T2 | Per-LLM statistics of holdout AUC | n, mean, sd, min, p10, median, p90, max, 95% CI, mean improvement, range, experiments per run, kept per run | `stats.py` | numbers in `01` |
| T3 | Head to head | pair, P(better wins), bootstrap interval, difference of means, (Welch p, Mann–Whitney p optional) | `stats.py` | numbers in `01` |
| T4 | Time course | per LLM: median time to first gain, median holdout at 15/30/45/60 min, experiments and keeps per run, AI share, median longest plateau, runs with ≥ 20-min plateau, mean steps down | `time_course.py` | numbers in `01` |
| T5 | Calendar audit | per LLM: dropped `DayofMonth` category, numeric day of year, holiday features, mean holdout dropped vs kept; plus first-move counts (shallower trees) | `feature_audit.py` + manual check | heuristic numbers in `01`; manual check owed |
| T6 | Best of k | per LLM, k = 1, 2, 3, 5, 10: median holdout of the chosen run, 5th/95th percentile; oracle column | `best_of_k.py` | simulated numbers in `01`; exact version owed |
| T7 | (Optional) Runs needed | observed gap, median sd, 16 sd²/gap² per arm, for the three pairs; labelled post hoc | `stats.py` | numbers in `01` |
| T8 | Validity summary | integrity flags raised / cleared, protocol caveats by kind, exclusions (0), leak-check hits, turns, clock stopped by, failed turns and retry waits, compactions, memory | `collect_runs.py`, `appendix_tables.py` | appendix |
| T9 | Per-run table (appendix) | 60 rows: run, experiments, kept, best eval AUC (commit), holdout AUC, gap, clock time, AI share, valid, caveat/flags | `appendix_tables.py` from `results_summary.md` | appendix |
| T10 | Sensitivity without caveat runs | T2 and T3 recomputed on the 50 runs without a caveat | `stats.py` | appendix |
| T11 | Eval–holdout gap | per LLM mean, sd, min, max; Spearman(eval, holdout) | `gap.py` | numbers in `01` |
| T12 | Tokens per run (appendix) | per LLM: input tokens, cached share, output tokens, reasoning tokens, API calls (mean, min, max); list-price projection per run | `tokens.py` | new |

Table T1 draft rows (verify each against the sources named):

| Item | Value |
|---|---|
| Task | predict `dep_delayed_15min` (departure delayed ≥ 15 min) from Month, DayofMonth, DayOfWeek, CRSDepTime, UniqueCarrier, Origin, Dest, Distance |
| Data | train: 200,000 flights of 2005, balanced; eval: 50,000 of 2006; holdout: 50,000 of 2006 (disjoint halves of one balanced sample); Data Expo 2009 airline data via the authors' S3 copy; `human/make_data.py`, seed 123 |
| Metric | AUC; the agent optimises eval AUC; every kept model scored on the holdout afterwards |
| Starter | XGBClassifier, 100 trees, depth 6, learning rate 0.1, native categoricals; eval 0.6743, holdout 0.6725 |
| Budget | 1 hour wall clock from `harness.py start`; training killed at 60 s, evaluation at 300 s; wrap up under 2 minutes |
| Keep rule | keep only a strictly higher eval AUC (4 decimals), or a tie with simpler or faster code |
| Agent | OpenAI Codex CLI 0.160.0, ChatGPT subscription, approvals and sandbox off inside the container, web search on |
| LLMs | gpt-6-luna, gpt-6-sol, gpt-6-astra; `model_reasoning_effort = max` (Luna's top level; Sol and Astra also have `ultra`) |
| Isolation | fresh `agents3` container per run (Ubuntu 26.04), minimal3 at `5fb023a` with fresh git history, human-only files root-only until the agent exits, 24 GB memory cap, no swap |
| Packages | xgboost 3.4.1, pandas 3.0.6, scikit-learn 1.9.1, numpy 2.5.3, cloudpickle 3.1.2 |
| Machine | one AWS m8i.2xlarge-class instance (8 vCPUs, 32 GB), runs sequential |
| Runs | 20 per LLM, 60 in all; Luna and Sol 2026-10-05 to 10-06, Astra 2026-10-06 to 10-07; 0 excluded, 10 with a protocol caveat |
| Orchestration | `/xgb-multi` skill in Claude Code: `run_one.sh` drives each run identically; checks, holdout scoring, leak check, archive; Claude reviews each run, authors review the reviews |
