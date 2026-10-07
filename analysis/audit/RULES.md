# Manual feature audit: rules

Date: 2026-10-07. The manual audit reads the final `train.py` of every run
(`xgboost-autoresearch-minimal3-runs/run-multi/<group>/<run>/train.py`, the code of the run's final model)
and confirms or corrects the scripted audit in `analysis/results/feature_audit_per_run.csv`. The verdicts
are recorded in `analysis/audit/<group>.csv` (one file per LLM), settled in `analysis/audit/verified.csv`,
and merged by `analysis/feature_audit.py`.

## What counts

Judge only what reaches the fitted model or models whose predictions `save_and_evaluate(model, prepare)`
scores: the columns `prepare()` returns and the model(s) fitted on them. Ignore comments, dead code,
helper functions that are never called, and variables that are computed but never passed to a model.

1. **dom_cat** (yes/no): yes if `DayofMonth` reaches any model of the final prediction as a categorical
   feature, that is, as a pandas category with XGBoost's native categorical support, or as one-hot or
   dummy columns of its levels. No if it is dropped, or reaches the model only as an ordered number
   (1 to 31), or only through derived features (day of year, holiday distances, week of month).
   Per-level encodings (a target, rate or frequency encoding of `DayofMonth` levels or of the month-day
   date) are not a category for this field, but must be named in the note.
2. **month_cat** (yes/no): the same for `Month`.
3. **doy** (yes/no): a numeric day-of-year-like feature reaches a model: day of year, days since a fixed
   date in the year, week or fortnight of the year, an ordinal date combining month and day into one
   ordered number, or a cyclic (sine/cosine) encoding of any of these. A numeric month alone, or a numeric
   day of month alone, does not count.
4. **holiday** (yes/no): at least one feature computed from holiday dates reaches a model: holiday flags,
   days to or from a holiday, holiday windows or travel seasons (Thanksgiving, Christmas, New Year,
   July 4, Memorial Day, Labor Day and the like). Holiday words in comments or unused code do not count.
5. **depth**: `max_depth` of each distinct model configuration in the final prediction, in the order of the
   file, separated by ", ". For lossguide trees with `max_depth` 0 or unset and `max_leaves` set, write
   "<n> leaves". Resolve values that the file computes from other variables; write "computed" only if the
   value cannot be resolved from the file. Write "6 (default)" if the parameter is never set.
6. **trees**: `n_estimators` (or `num_boost_round`) per configuration, same convention ("100 (default)").
7. **learning_rate**: `learning_rate` or `eta` per configuration, same convention ("0.3 (default)").
8. **ensemble** (yes/no): yes if the final prediction combines the predictions of more than one fitted
   model: different configurations, seed averaging, bagging or a blend. A single booster with
   `num_parallel_tree` > 1 is one model (no), but say so in the note.

## Output, one row per run

`run, dom_cat, month_cat, doy, holiday, depth, trees, learning_rate, ensemble, disagrees_with_script, evidence, note`

- `disagrees_with_script`: the fields whose verdict differs from the script's row, separated by spaces
  (`dom_cat month_cat doy holiday depth trees learning_rate ensemble`), or `none`. For depth, trees and
  learning rate, compare with the script's `max_depth_all`/`max_leaves_all`, `n_estimators_all` and
  `learning_rate_all`.
- `evidence`: line numbers in `train.py` for each of the four calendar verdicts, e.g.
  `dom_cat: L31 cat_cols, L64 drop; month_cat: L31; doy: L45 day_of_year; holiday: none`.
- `note`: per-level encodings, ambiguities, anything a reader of Table 6 or Table 13 should know; empty if
  nothing.
