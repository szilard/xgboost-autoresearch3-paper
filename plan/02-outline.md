# 02. Section-by-section outline

Length: no upper limit (decision 18 in 08); the per-section page counts below were the first draft's guide, not caps. Single-column arXiv preprint, plus appendix. Write in
this order: Methods, Results, Related work, Introduction, Discussion, Conclusion, Abstract.

## Abstract (150 to 200 words)

Draft, to be tightened once the results section is final:

> AI coding agents can automate much of a data scientist's trial-and-error work, but their runs
> are not deterministic: the same agent given the same task twice tries different ideas in a
> different order and ends with a different model. We measure how much that matters. An agent
> (OpenAI Codex) was given one hour, identical instructions and a fresh isolated container to
> improve a starter XGBoost model that predicts flight delays, trained on 2005 flights and
> evaluated on 2006 flights, with every kept model scored afterwards on a holdout set the agent
> never sees. We ran it 20 times with each of three LLMs (gpt-6-luna, gpt-6-sol, gpt-6-astra) at
> their "max" reasoning effort, 60 runs in all, with automatic integrity checks; no run had to be
> excluded. Every run improved the starter model, and the three LLMs rank clearly on average
> (holdout AUC 0.6806, 0.6842, 0.6866; 95% confidence intervals disjoint). But the spread within an
> LLM, 0.007 to 0.009 AUC from worst to best run, is larger than the 0.006 between the best and
> the worst LLM's means, the ranges overlap, and one run of each ranks the two closest LLMs
> wrongly one time in five. We show how the variation builds up over the hour, trace part of the
> gap between LLMs to how they handle the calendar, and conclude that comparisons of agents, LLMs
> or prompts need repeated runs and distributions, while a good model is best obtained by running
> several times and selecting on unseen data. The single-run building block and the multi-run
> orchestrator are open source.

## 1. Introduction (1.5 to 2 pages)

- Open with the previous project (Pafka and Ariño de la Rubia 2026, `pafka2026autoresearch`): an
  agent researches ideas, engineers features, tunes XGBoost, keeps what works; the earlier
  results came from single runs of a single agent.
- The problem: agents are not deterministic; a single run is one sample from a wide range of
  outcomes, so it cannot say how good a setup is or whether one LLM beats another. State that
  run-to-run variation of LLM agents is known in the literature (cite τ-bench pass^k, Bjarnason et
  al. 2026, MLE-bench's three-seed guidance, Rabanser et al. 2026) and that what is missing for a
  data scientist is its size on a continuous measure of the delivered model under a fixed,
  audited protocol, across LLMs of different strength.
- What we did: rebuilt the project into a minimal building block plus an orchestrator; 3 LLMs x
  20 runs; the task in two sentences; the holdout.
- Contributions list (from `01-main-points.md`).
- Headline findings in one paragraph, with the three means, the ranges, and the 98 / 91 / 80%.
- Roadmap sentence.

## 2. Related work (1.5 to 2 pages)

Themes and citations in `05-related-work.md`. Subsections:

2.1 Agents that do machine-learning engineering (autoresearch lineage; benchmarks; LLMs for HPO).
2.2 Variation between identical runs of LLMs and agents (nondeterminism of LLM outputs and its
    sources; agent reliability metrics; repeated-run studies; older ML/RL seed-variance work).
2.3 Statistics of comparing noisy systems and of selecting among attempts (error bars and power;
    probability of superiority; best-of-k and repeated sampling; selection and holdout reuse).
2.4 Evaluating agents and models as deployed systems; rule-following (harness-model pairing; the
    companion paper, by design only; reward hacking and public-score exploitation as the
    motivation for the integrity checks).
2.5 Tabular learning and temporal shift (why XGBoost; why train on 2005 and test on 2006).

Close with the positioning paragraph: the pieces are known; this paper measures them together,
on one task, one agent, three frontier LLMs, 20 identical runs each, with a time-resolved view of
each run and an audit of what the runs actually changed.

## 3. Methods (3 to 4 pages)

3.1 **Task and data.** Airline on-time data (Data Expo 2009) read from the authors' S3 copy by
    `human/make_data.py`: flights that departed; label `dep_delayed_15min` (DepDelay >= 15);
    eight predictors known before departure (Month, DayofMonth, DayOfWeek as `c-` strings;
    CRSDepTime, Distance numeric; UniqueCarrier, Origin, Dest); train = 200,000 rows sampled from
    2005, balanced (100,000 per class, seed 123); one balanced 100,000-row sample from 2006 split
    into eval (50,000) and holdout (50,000), disjoint; metric AUC. Note the deliberate year shift
    and the sentence in `program.md` telling the agent about it. State the AUC sampling error
    (about 0.002 per set; Hanley–McNeil with 25,000 per class) and that eval and holdout are
    paired samples of the same year.

3.2 **The starter model and the editable file.** `train.py`: pandas categoricals with levels
    fixed on train, XGBClassifier with 100 trees, depth 6, learning rate 0.1,
    `enable_categorical`, seed 42; starter eval 0.6743 / holdout 0.6725. `prepare(df)` must be
    row-local; lookups fitted on train at module level.

3.3 **The harness and the rules** (`harness.py`, `program.md`). Clock of 1 hour; `harness.py run`
    times `train.py`, kills training after 60 s and evaluation after 300 s, refuses once the
    budget is up; artifact (model + `prepare`, cloudpickle) saved per commit; eval set scored one
    row at a time across processes so batch-dependent features cannot work; keep rule (strictly
    higher eval AUC at 4 decimals, or equal with simpler or faster code); discard = git reset; log
    to `results.tsv` and a research log; mandatory web research; forbidden: anything in `human/`,
    the holdout set, the source CSVs, other data, new packages, changes to the evaluation; wrap-up
    when under 2 minutes remain; stop the clock. Quote the keep rule verbatim. (The hand-run
    test runs in the minimal3 repo and the orchestrator's `archive/test1` are not mentioned:
    authors' decision.)

3.4 **The orchestrator and isolation** (`xgboost-autoresearch-minimal3-runs`). `agents3` Docker
    image: Ubuntu 26.04, codex installed as an unprivileged user, Python packages (versions:
    xgboost 3.4.1, pandas 3.0.6, scikit-learn 1.9.1, numpy 2.5.3, cloudpickle 3.1.2), a clone of
    minimal3 at `5fb023a` with fresh git history and no `results/`; `human/` scripts and
    `holdout.csv` moved to a root-only directory and copied back only after the agent exits; only
    the ChatGPT login shared through a volume. Container per run with a 24 GB memory cap and no
    swap. The driver `run_one.sh`: preconditions, setup check of the starter (eval 0.6743
    expected), model and effort level verified from the codex catalogue, `codex exec` turns with
    the README prompt, then "go" until the clock starts and "keep going" if the agent stops early;
    the harness enforces the hour; retries on capacity errors (30 s) and other failures (5 min)
    with limits; after the agent exits: harness report, `run_checks.py`, holdout scoring of every
    kept commit, `leak_check.py` on the session log, archive, delete the container. Claude Code
    reviewed each run (the `/xgb-multi` skill) and wrote `run.md`; the authors reviewed the
    reviews. Runs sequential (each uses all 8 cores) on one m8i.2xlarge-class machine (8 cores,
    30 GB visible).

3.5 **Agent, LLMs, settings.** Codex CLI 0.160.0 on a ChatGPT subscription; gpt-6-luna, gpt-6-sol,
    gpt-6-astra; `model_reasoning_effort = max` (Luna's top level; in Codex's model catalogue
    Sol and Astra list `ultra` above it, while OpenAI's API model pages list `max` as the top
    level for all three; `turn_context` confirmed from every session log); approvals off, sandbox
    off inside the container; web search on (the instructions require it). Cite the model pages
    and the Codex configuration reference (keys in `references.bib`). Dates: Luna and Sol runs
    2026-10-05 to 10-06, Astra 2026-10-06 to 10-07. State plainly that the hosted service's
    builds, load and routing are not under our control and that the measured variation is that of
    the deployed agent–LLM–service system.

3.6 **Validity checks.** Integrity checks (exclude on failure): only `train.py` changed; no
    modified harness; no extra data files; every artifact and kept row from a harness run inside
    the clock; `train.py` reads nothing but `train.csv`; no download of flight data; no content
    of the holdout set, the eval set or the human-only scripts in the session log. Protocol checks
    (caveat, run stays valid): keep rule, missed resets, branch order, early stop, outputs
    committed, stray files, driver had to stop the clock, retry waits over 2 minutes, forbidden
    attempts. The eval–holdout gap reported for every run with provisional thresholds (−0.006 /
    +0.003). Outcome: 0 excluded, 10 flags cleared, 10 caveats (list).

3.7 **Outcome measures and statistics.** Primary outcome: holdout AUC of the final model (best
    eval AUC; tie → last kept). Per LLM: n, mean, sample SD, min, 10th/90th percentile (nearest
    run), median, max, 95% t-interval of the mean. Head to head: probability of superiority over
    all run pairs, ties half (Mann–Whitney / Vargha–Delaney A), 95% percentile bootstrap (runs
    resampled per LLM, 10,000 resamples, seed 1). Paths: holdout AUC of the kept model from the
    end of its harness run until the next keep, minutes since the clock started; median path at
    each time over the LLM's runs, a finished run counting with its final value. Feature audit:
    scripted parse of each final `train.py` plus manual check. Best-of-k: choose on eval AUC
    among k draws with replacement, report the holdout AUC of the chosen run (exact or simulated).
    All runs included, caveat runs alike; sensitivity without caveat runs in the appendix. Label
    the power approximation and the best-of-k as post hoc.

## 4. Results (4 to 5 pages)

4.1 **All runs improve; the LLMs rank on average.** Figure 1 (beeswarm), Table 2 (per-LLM
    statistics). Claims 1 and 2 of `01`.
4.2 **Runs of one LLM vary as much as LLMs differ.** Ranges, percentiles, overlap statements
    (Claim 3). Keep the three "best run of X beats N runs of Y" sentences.
4.3 **One run of each ranks two LLMs wrong surprisingly often.** Figure 2 (head to head),
    Table 3. Claim 4. Optionally the runs-per-arm approximation, flagged post hoc.
4.4 **How the variation builds up over the hour.** Figures 3 and 4 (paths), Table 4 (time-course
    summary). Claim 5: the common first move; first gain times; medians at 15/30/45/60; the
    second half hour; experiments per run; plateaus; steps down on holdout.
4.5 **What the LLMs changed: the calendar.** Table 5 (feature audit). Claim 6 with the luck
    caveat (Astra's weakest run).
4.6 **Selection on the eval set and the holdout** (short). Gap statistics; Spearman between eval
    and holdout AUC; Figure 5 (eval vs holdout scatter) if included.
4.7 **Several runs, pick the best** (short). Best-of-k table (Table 6), with the caveat that it
    is computed on the same 20 runs and the ceiling is the observed maximum.
4.8 **Validity of the runs** (short, can be merged into 3.6 or the appendix). No exclusions; the
    cleared flags; the caveats; the BTS and HP→US notes; sensitivity without caveat runs.

## 5. Discussion (1.5 to 2 pages)

- What the variation means for comparing agents, LLMs, prompts and other parts of a setup: a
  single run is one draw; report distributions; the number of runs depends on the gap one wants to
  see (illustrate with the observed gaps; post hoc).
- What it means for getting a good model: run several times, select on unseen data, confirm on
  untouched data; the selection bias of picking the best of k on the eval set and why a third set
  is needed (cite Cawley and Talbot; Dwork; note that here the eval–holdout rank correlation is
  high).
- Why the LLMs differ: more experiments per hour (Sol and Astra 45 to 47 against Luna's 30),
  earlier first gains, the calendar decision, holiday features, longer sustained climbing (Astra
  in the second half hour); and why runs of one LLM differ: which ideas are tried, in what order,
  how they are followed up; plateaus.
- Effort and model tiers: all at "max"; Sol and Astra have "ultra" above; the comparison is at a
  named setting, not at each model's ceiling.
- The eval–holdout gap: small and stable for Luna and Sol, larger for Astra; what it says about
  overfitting the eval set under a strict keep rule with 30 to 70 experiments.
- Design choices that made the study possible: a fixed hour instead of a fixed number of
  experiments (so faster models run more experiments: this is part of what is being compared);
  row-by-row scoring; the holdout out of reach; automated review; everything open.
- Relation to the companion paper: one sentence, design-level, no numbers (see `05`).
- Limitations: one agent (Codex), one vendor's LLMs, one task and dataset, one hour, one effort
  setting, n = 20 per LLM, three days of runs through a hosted service that can change, holdout
  from the same year as the eval set, web research allowed (two runs used BTS documentation about
  2006 carrier reporting; reported, kept), feature audit partly heuristic, the orchestrator's
  reviewer was itself an LLM (Claude Code) with human oversight.
- Future work: more agents and LLMs, prompts and effort levels through the same orchestrator;
  score the 60 final models on 2007 flights (new computation); larger n for the close pairs; other
  tasks and datasets; cost from session-log usage.

## 6. Conclusion (half a page)

The blog's closing paragraph, tightened: agents consistently improve the model (60 of 60), the
size varies a lot between identical runs, two consequences (repeated runs and distributions for
comparisons; several runs plus selection on unseen data plus confirmation on untouched data for a
good model), both tools open source.

## References

From `references.bib`; natbib author-year or numeric (decide in `08`).

## Appendix

A. Per-run table: 60 rows (run, LLM, experiments, kept, best eval AUC and commit, holdout AUC,
   gap, clock time, AI share, valid, caveat/flags) from the three `results_summary.md`.
B. Validity checks in detail: the ten integrity flags and their resolution; the ten caveats; the
   leak-check method; the "for the human to judge" items; sensitivity analysis without caveat runs
   (means, win probabilities).
C. The agent instructions: `program.md` verbatim (or its rules section) and the README prompt;
   the driver's turn messages.
D. Statistics details: bootstrap procedure; the median-path definition; the best-of-k formula;
   the power approximation; Welch and Mann–Whitney results.
E. Feature audit method and the per-run audit table (what each final model does with Month,
   DayofMonth, holidays, day of year, tree depth, trees, learning rate, ensembles).
F. Software versions, machine, dates, container settings; repository and commit list; data
   availability (S3 source, `make_data.py`); AI-assistance disclosure.
H. Token usage per run from the session logs (input, cached share, output, reasoning), per LLM
   mean and range, with a list-price projection labelled as a projection (Table T12).
G. (Optional) Example run: the kept-commit history of one run (e.g. astra6_n20-1 or -13) with
   eval and holdout AUC per keep, to show what an hour looks like.
