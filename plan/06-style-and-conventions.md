# 06. Style and conventions

## Voice

The blog post's voice: plain, concrete, short sentences, numbers in context, no hype, every
statement tied to something measured. Keep it. Prefer "we ran", "the agent kept", "the median".
No em-dashes. Spell out what a plot shows before interpreting it. Say "one run is not enough",
not "our novel framework demonstrates".

## Terminology (fix once, use everywhere)

| Term | Meaning | Avoid |
|---|---|---|
| **LLM** | the language model (gpt-6-luna, gpt-6-sol, gpt-6-astra) | "model" for the LLM in prose (the runs repo's tables say "model"; the paper's prose and new tables should say LLM; figure labels may keep the slugs) |
| **model** | an XGBoost model | |
| **agent** | OpenAI Codex (the CLI agent, codex-cli 0.160.0), the same in every run | "harness" for Codex (keep "harness" for `harness.py`) |
| **the harness** | `harness.py` (clock, timed runs, artifact, row-by-row scoring) | |
| **run** | one hour-long session of the agent, from "go" to the clock stop | "trial", "seed", "attempt" (use "attempt" only in the best-of-k discussion) |
| **experiment** | one timed execution of `train.py` through the harness; a row of `results.tsv`; the baseline counts | "run" for an experiment |
| **kept / discarded / crashed** | the status of an experiment under the keep rule | |
| **starter model** | the `train.py` as shipped (0.6743 eval, 0.6725 holdout) | "baseline" in prose (the agent's logs say baseline; fine in tables) |
| **final model** | a run's kept model with the highest eval AUC (tie: last kept) | "best model" (ambiguous with the best on holdout) |
| **eval set / eval AUC** | the 50,000 2006 rows the agent optimises on | "validation", "test" |
| **holdout set / holdout AUC** | the 50,000 2006 rows scored after the run | "test set" |
| **gap** | holdout AUC − eval AUC of the final model | |
| **Luna, Sol, Astra** | short names after the first mention of the slugs | "GPT-6 Luna" in prose unless quoting the vendor |
| **"max"** | the effort level literally named max; Luna's highest; Sol and Astra also have "ultra" | "maximum effort" |
| **caveat run** | valid run with a protocol caveat (kept tie not simpler or faster; retry waits over 2 minutes) | "flagged" (integrity flags were all cleared) |

## Numbers

- AUC and AUC differences: 4 decimals (0.6866, +0.0024). In prose, approximate differences may be
  given as "about 0.003". Percentages for win probabilities: whole numbers (98%, 91%, 80%).
- Times: minutes with one decimal in tables, whole minutes in prose. Hours as "1 hour".
- Always say what a mean is a mean of (holdout AUC of the final model, over 20 runs).
- Confidence intervals: "95% confidence interval (t distribution, n = 20)". Bootstrap: "95%
  percentile bootstrap, 10,000 resamples".
- Every number in the text must appear in a committed results file; prefer tables over inline
  number lists.
- Label post hoc analyses as post hoc (power approximation, best-of-k, the correlation of
  experiments with holdout AUC).

## Caveats and integrity

- State once in methods and once in the appendix: 0 excluded; 10 integrity flags, all false
  alarms on review (list); 10 caveat runs (list); all 60 analysed alike; sensitivity table without
  caveat runs in the appendix.
- Describe the web-research observations (BTS pages; the HP→US mapping) factually and briefly:
  calendar and documentation, no flight records, eval set never read; they are reported, not
  excluded.
- Do not call the agent's behaviour "cheating" anywhere; nothing of the kind was found.

## Figures

- One colour per LLM, fixed (see `04`). Rows and legends ordered Astra, Sol, Luna (best mean on
  top), as in the blog.
- Vector PDF; sans-serif; axis label "holdout AUC"; x-axis of path plots "minutes since the clock
  started".
- Each figure referenced in the text before it appears; captions self-contained.

## Disclosure, licence, data

- Disclosure paragraph (appendix F): Claude Code, running the `/xgb-multi` skill, launched the
  runs through a fixed driver script, reviewed each finished run against the checks and drafted
  its `run.md`; Claude also helped write the tools, the blog post and this paper. Codex (the agent
  under study) did the modelling in every run. The authors designed the study, reviewed every
  run's review, and are responsible for the text and the numbers.
- Licence: the blog is CC BY 4.0; use the same for the paper (arXiv licence choice CC BY 4.0).
- Data availability: the airline data are public (Data Expo 2009); `human/make_data.py` rebuilds
  the splits from the authors' S3 copy with fixed seeds; the 60 runs' logs, results and final
  `train.py` files are in the runs repo at the pinned commit; model artifacts were not kept.

## Consistency pass before submission

The blog went through several rounds of "fix inconsistencies" and "clarity fixes after an
independent read" (see its git log). Plan the same: one pass by an author who did not write the
section, one automated pass that checks every number in the `.tex` against `analysis/results/`,
and one read of the abstract against the results tables.
