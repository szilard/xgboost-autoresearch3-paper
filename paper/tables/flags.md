| run | integrity flag (cleared) | caveat | resolution |
|----------------------|----------------------------------|---------------------|--------------------------------------------------|
| astra6_n20-4 | artifact_outside_clock |  | explained: the last experiment, started inside the clock with 1m53s left, was cut off during evaluation when the turn failed |
| astra6_n20-5 |  | keep_rule | `7b7712f` (gamma 5) kept at a tie as "faster" by 0.8 s, within noise, not simpler; gamma 5 stayed in the final model |
| astra6_n20-6 | leak_check_hit |  | false match: the leak check matched the end of a column list that the agent printed in its own setup check |
| astra6_n20-8 | leak_check_hit | keep_rule | false match: the leak check matched a call to the harness's own artifact loader in the agent's final check; `e5e4a2b` (`max_cat_threshold` 16) kept at a tie, 0.2 s faster, not simpler; it stayed in the final model |
| astra6_n20-12 |  | keep_rule | `d4bd0fc` (`max_bin` 64) kept at a tie for 1.1 s in one timing, not simpler; it stayed in the final model |
| astra6_n20-15 | train_py_review |  | explained: a read of `data/train.csv` written differently from the starter, in a discarded commit |
| astra6_n20-16 | artifact_outside_clock |  | explained: the agent reset the repository before the evaluation of a discarded commit had finished, so its timing row carries the wrong commit |
| sol6_n20-8 |  | keep_rule | `83775c5` (DART `rate_drop` 0.2) kept at a tie as "faster" by 1.0 s, within noise, not simpler; it is the final model |
| sol6_n20-12 | train_py_review |  | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`) |
| sol6_n20-16 |  | turn_retries | 7 failed turns, all 'model at capacity'; retry waits of 216 s |
| sol6_n20-19 |  | keep_rule | `f833740` (lossguide tree growth) kept at a tie as "faster" by 1.0 s, within noise, not simpler; lossguide stayed in the final model |
| luna6_n20-1 | train_py_review |  | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`) |
| luna6_n20-6 |  | keep_rule | `bd192f4` (gamma 0.1) kept at a tie, for an evaluation 0.6 s faster, within noise; the commit before it has the same eval and holdout AUC |
| luna6_n20-7 | train_py_review |  | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`) |
| luna6_n20-8 |  | keep_rule | two ties kept for a faster run that is noise (`744ceef`, `7a1cbf0`, `min_child_weight` 5 and 10); each has the same eval and holdout AUC as the commit before it |
| luna6_n20-11 | train_py_review |  | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`) |
| luna6_n20-15 | train_py_review | keep_rule | false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`); two ties kept for a faster run that is noise (`744705b`, `41db4a7`, gamma 1 and 2); same eval and holdout AUC as the commit before them, but gamma 2 stayed in the final model |
| luna6_n20-18 |  | keep_rule | `dfccd9c` (gamma 1) kept at a tie for an evaluation 0.3 s faster, within noise; the commit before it has the same eval and holdout AUC. Needed a second "go" |

Table: The runs with an integrity flag from the automatic checks or a content hit in the leak check (all cleared on review), or a protocol caveat. No run was excluded.
