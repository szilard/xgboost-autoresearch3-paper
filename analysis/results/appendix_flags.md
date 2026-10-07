<!-- analysis/appendix_tables.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ b2841ab; generated 2026-10-07 16:11Z -->

## Runs with integrity flags (all cleared on review) or protocol caveats

| run | integrity flags (run_checks.py) | protocol flags (run_checks.py) | valid | caveat flags (review) | review note |
|--------------------|--------------------------------|----------------------|-----------|-------------------|--------------------------------------------------|
| astra6_n20-4 | artifact_outside_clock | none | yes |  | explained: the last experiment, started inside the clock with 1m53s left, was cut off during evaluation when the turn failed |
| astra6_n20-5 | none | none | caveat | keep_rule | caveat: `keep_rule`: `7b7712f` (gamma 5) kept at a tie as "faster" by 0.8 s, within noise, not simpler; gamma 5 stayed in the best model |
| astra6_n20-6 | leak_check_hit | none | yes |  | false match: the leak check matched the end of a column list that the agent printed in its own setup check |
| astra6_n20-8 | leak_check_hit | none | caveat | keep_rule | false match: the leak check matched a call to the harness's own artifact loader in the agent's final check; caveat: `keep_rule`: `e5e4a2b` (`max_cat_threshold` 16) kept at a tie, 0.2 s faster, not simpler; it stayed in the best model |
| astra6_n20-12 | none | none | caveat | keep_rule | caveat: `keep_rule`: `d4bd0fc` (`max_bin` 64) kept at a tie for 1.1 s in one timing, not simpler; it stayed in the best model |
| astra6_n20-15 | train_py_review | none | yes |  | explained: a read of `data/train.csv` written differently from the starter, in a discarded commit |
| astra6_n20-16 | artifact_outside_clock | none | yes |  | explained: the agent reset the repository before the evaluation of a discarded commit had finished, so its timing row carries the wrong commit |
| sol6_n20-8 | none | none | caveat | keep_rule | caveat: keep_rule (tie kept as "faster" by 1.0 s, not simpler) |
| sol6_n20-12 | train_py_review | none | yes |  | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`) |
| sol6_n20-16 | none | none | caveat | turn_retries | caveat: turn_retries (7 failed turns, model at capacity; retry waits 216 s) |
| sol6_n20-19 | none | none | caveat | keep_rule | caveat: keep_rule (tie kept as "faster" by 1.0 s, not simpler) |
| luna6_n20-1 | train_py_review | none | yes |  | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`) |
| luna6_n20-6 | none | none | caveat | keep_rule | caveat: `keep_rule`: `bd192f4` (gamma 0.1) kept at a tie, for an evaluation 0.6 s faster, within noise; the commit before it has the same Eval and Holdout AUC |
| luna6_n20-7 | train_py_review | none | yes |  | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`) |
| luna6_n20-8 | none | none | caveat | keep_rule | caveat: `keep_rule`: two ties kept for a faster run that is noise (`744ceef`, `7a1cbf0`, `min_child_weight` 5 and 10); each has the same Eval and Holdout AUC as the commit before it |
| luna6_n20-11 | train_py_review | none | yes |  | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`) |
| luna6_n20-15 | train_py_review | none | caveat | keep_rule | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`); caveat: `keep_rule`: two ties kept for a faster run that is noise (`744705b`, `41db4a7`, gamma 1 and 2); same Eval and Holdout AUC as the commit before them, but gamma 2 stayed in the best model |
| luna6_n20-18 | none | none | caveat | keep_rule | caveat: `keep_rule`: `dfccd9c` (gamma 1) kept at a tie for an evaluation 0.3 s faster, within noise; the commit before it has the same Eval and Holdout AUC. Needed a second "go" |

## Operational summary per LLM

| LLM | turns sent beyond the prompt and one go (retries included) | failed turns | runs with retry waits | runs where the driver stopped the clock | runs that stopped after the budget | runs with a context compaction | peak memory, GiB | processes killed at the cap |
|---------|--------------|----------|--------|-----------|-----------|---------------|-----------|--------------|
| Astra | 1 | 1 | 1 | 0 | 4 | 11 | 3.4 to 16.5 | 0 |
| Sol | 12 | 13 | 4 | 0 | 2 | 2 | 3.6 to 11.7 | 0 |
| Luna | 1 | 0 | 0 | 0 | 0 | 12 | 3.6 to 12.0 | 0 |
