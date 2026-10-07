# Manual feature audit: how the verdicts were settled (2026-10-07)

Every final `train.py` was read in full by one of three Claude agents (one per LLM) under `RULES.md`; their
verdicts are in `astra6_n20.csv`, `sol6_n20.csv` and `luna6_n20.csv`, with line-number evidence. The
orchestrating Claude session then read, in the files themselves:

- the ten files the script had flagged as possibly misread: astra6_n20-11 and -16 (DayofMonth used inside
  `prepare` only for holiday flags or a capped holiday distance, so not a category); sol6_n20-2, -4, -5, -6,
  -9, -17 and luna6_n20-16, -19 (DayofMonth both in the category list and converted to a number: in all
  eight the categorical column reaches the model, and the numeric day only feeds a day-of-year or holiday
  feature);
- every file where a reader disagreed with the script on a calendar field: astra6_n20-3, -4, -8, -12, -14,
  -18, -19 and -16 (a variable named `day_of_year` or `doy` that only feeds holiday offsets capped at 7 to
  21 days, never a model column, so no day-of-year-like feature), sol6_n20-12 (Month copied into a
  categorical column named `MonthCategory`) and sol6_n20-8 (a year-end travel window, 21 December to
  6 January, used as a feature).

All readers' calendar verdicts were confirmed. One bookkeeping slip was found: the astra6_n20-16 row said
no disagreement although its day-of-year verdict differs from the script's; `settle.py` therefore
recomputes all disagreements from the script's values. `settle.py` writes `verified.csv`, which
`analysis/feature_audit.py` merges over the script's verdicts (the script's own values stay in the
`script_*` columns of `results/feature_audit_per_run.csv`).

Corrections (20 files): day-of-year-like feature 8 (all Astra, yes to no), Month category 1 (sol6_n20-12,
no to yes), holiday features 1 (sol6_n20-8, no to yes), ensemble 11 (eight Astra files with a single booster and
`num_parallel_tree` > 1, one model under the rules, and astra6_n20-3, -11 and sol6_n20-8 blend or
average several models), and model settings of ensembles the script read only in part. No DayofMonth
verdict changed.
