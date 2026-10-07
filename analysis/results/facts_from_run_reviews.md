<!-- hand-collected from the runs repo's review files; each line names its source -->

# Facts quoted in the paper that come from the run reviews or are derived from the tables

| fact | value | source |
|---|---|---|
| HP-to-US carrier mapping, gain on holdout when made, astra6_n20-7 | +0.0004 (eval +0.0001) | run-multi/astra6_n20/results_summary.md, "Per-run details" |
| HP-to-US carrier mapping, gain on holdout when made, astra6_n20-12 | +0.0007 (eval +0.0003) | run-multi/astra6_n20/results_summary.md, "Per-run details" |
| Holiday windows from the TranStats table, astra6_n20-12 | +0.0016 on eval | same |
| Largest move of any LLM's mean when the caveat runs or the BTS-informed runs are left out | 0.0002 (Astra 0.6866 to 0.6864 without Astra 7 and 12; 0.6867 without the caveat runs) | sensitivity.md |
| Range of P(Astra beats Sol) across the three subsets | 78% to 82% | sensitivity.md |
| Astra's weakest run | astra6_n20-4, holdout 0.6815, dropped DayofMonth category, holiday features | feature_audit_per_run.csv |
| Context compactions | 11 Astra, 2 Sol, 12 Luna runs; 25 in all | runs.csv (compactions column) |
| Runs that ended their wrap-up after the budget | 4 Astra, 2 Sol, 0 Luna | runs.csv (clock_remaining_s < 0) |
| Runs with service errors resumed by the driver | astra6_n20-4, sol6_n20-4, sol6_n20-16, sol6_n20-17, sol6_n20-20 | runs.csv (failed_turns) |
