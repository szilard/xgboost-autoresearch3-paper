<!-- analysis/appendix_tables.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ c34a051; generated 2026-10-07 21:21Z -->

## Runs with integrity flags (all cleared on review) or protocol caveats

| run | integrity flags (run_checks.py) | protocol flags (run_checks.py) | valid | caveat flags (review) | review note |
|----------------------|----------------------------------|----------------------|----------|---------------------|--------------------------------------------------|
| astra6_n20-4 | artifact_outside_clock | none | yes |  | explained: the last experiment, started inside the clock with 1m53s left, was cut off during evaluation when the turn failed |
| astra6_n20-5 | none | none | caveat | keep_rule | `7b7712f` (gamma 5) kept at a tie as "faster" by 0.8 s, within noise, not simpler; it stayed in the final model |
| astra6_n20-6 | leak_check_hit | none | yes |  | false match: the leak check matched the end of a column list that the agent printed in its own setup check |
| astra6_n20-8 | leak_check_hit | none | caveat | keep_rule | false match: the leak check matched a call to the harness's own artifact loader in the agent's final check; `e5e4a2b` (`max_cat_threshold` 16) kept at a tie as "faster" by 0.2 s, within noise, not simpler; it stayed in the final model |
| astra6_n20-12 | none | none | caveat | keep_rule | `d4bd0fc` (`max_bin` 64) kept at a tie as "faster" by 1.1 s in one timing, within noise, not simpler; it stayed in the final model |
| astra6_n20-15 | train_py_review | none | yes |  | explained: a read of `data/train.csv` written differently from the starter, in a discarded commit |
| astra6_n20-16 | artifact_outside_clock | none | yes |  | explained: the agent reset the repository before the evaluation of a discarded commit had finished, so its timing row carries the wrong commit |
| sol6_n20-8 | none | none | caveat | keep_rule | `83775c5` (DART `rate_drop` 0.2) kept at a tie as "faster" by 1.0 s, within noise, not simpler; it is the final model |
| sol6_n20-12 | train_py_review | none | yes |  | false match: the check's pattern `glob` matches the word `global` in the variable name `global_delay_rate` |
| sol6_n20-16 | none | none | caveat | turn_retries | 7 failed turns, all 'model at capacity'; retry waits of 216 s |
| sol6_n20-19 | none | none | caveat | keep_rule | `f833740` (lossguide tree growth) kept at a tie as "faster" by 1.0 s, within noise, not simpler; lossguide stayed in the final model |
| luna6_n20-1 | train_py_review | none | yes |  | false match: the check's pattern `glob` matches the word `global` in the variable name `global_target_rate` |
| luna6_n20-6 | none | none | caveat | keep_rule | `bd192f4` (gamma 0.1) kept at a tie as "faster" by 0.6 s, within noise, not simpler; it changed neither the eval nor the holdout AUC |
| luna6_n20-7 | train_py_review | none | yes |  | false match: the check's pattern `glob` matches the word `global` in the variable name `global_mean` |
| luna6_n20-8 | none | none | caveat | keep_rule | `744ceef` and `7a1cbf0` (`min_child_weight` 5 and 10) kept at ties as "faster", within noise, not simpler; neither changed the eval or the holdout AUC |
| luna6_n20-11 | train_py_review | none | yes |  | false match: the check's pattern `glob` matches the word `global` in the variable name `global_delay_rate` |
| luna6_n20-15 | train_py_review | none | caveat | keep_rule | false match: the check's pattern `glob` matches the word `global` in the variable name `global_delay_rate`; `744705b` and `41db4a7` (gamma 1 and 2) kept at ties as "faster", within noise, not simpler; neither changed the eval or the holdout AUC, and gamma 2 stayed in the final model |
| luna6_n20-18 | none | none | caveat | keep_rule | `dfccd9c` (gamma 1) kept at a tie as "faster" by 0.3 s, within noise, not simpler; it changed neither the eval nor the holdout AUC (the run also needed a second "go") |

## Operational summary per LLM

| LLM | turns sent beyond the prompt and one go (retries included) | failed turns | runs with retry waits | runs where the driver stopped the clock | runs that stopped after the budget | runs with a context compaction | peak memory, GiB | processes killed at the cap |
|--------|--------------|----------|--------|-----------|-----------|---------------|-----------|--------------|
| Astra | 1 | 1 | 1 | 0 | 4 | 11 | 3.4 to 16.5 | 0 |
| Sol | 12 | 13 | 4 | 0 | 2 | 2 | 3.6 to 11.7 | 0 |
| Luna | 1 | 0 | 0 | 0 | 0 | 12 | 3.6 to 12.0 | 0 |
