<!-- hand-collected from the runs repo's review files; each line names its source -->

# Facts quoted in the paper that come from the run reviews or are derived from the tables

| fact | value | source |
|---|---|---|
| HP-to-US carrier mapping, gain on holdout when made, astra6_n20-7 | +0.0004 (eval +0.0001) | run-multi/astra6_n20/results_summary.md, "Per-run details" |
| HP-to-US carrier mapping, gain on holdout when made, astra6_n20-12 | +0.0007 (eval +0.0003) | run-multi/astra6_n20/results_summary.md, "Per-run details" |
| Holiday windows from the TranStats table, astra6_n20-12 | +0.0016 on eval | same |
| Largest move of any LLM's mean when the caveat runs or the BTS-informed runs are left out | 0.0002 (Astra 0.6866 to 0.6864 without Astra 7 and 12; 0.6867 without the caveat runs) | sensitivity.md |
| Range of P(Astra beats Sol) across the three subsets | 79% to 82% | sensitivity.md |
| Astra's weakest run | astra6_n20-4, holdout 0.6815, dropped DayofMonth category, holiday features | feature_audit_per_run.csv |
| Context compactions | 11 Astra, 2 Sol, 12 Luna runs; 25 in all | runs.csv (compactions column) |
| Runs that ended their wrap-up after the budget | 4 Astra, 2 Sol, 0 Luna | runs.csv (clock_remaining_s < 0) |
| Runs with service errors resumed by the driver | astra6_n20-4, sol6_n20-4, sol6_n20-16, sol6_n20-17, sol6_n20-20 | runs.csv (failed_turns) |
| Gap thresholds of the run review (holdout minus eval AUC of the final model): overfit below, recheck above | -0.006 / +0.003; set 2026-10-04 (runs repo commit cc132e5), unchanged during the runs, no run crossed either | .claude/skills/xgb-multi/SKILL.md in the runs repo; run-multi/{luna6_n20,sol6_n20,astra6_n20}/results_summary.md, "Gaps" |
| Six Sol runs tried more trees at the starter's learning rate among their first three experiments; eval AUC change against the baseline | -0.0061 to -0.0091 (sol6_n20-1, -4, -5, -6, -9, -12), all discarded | run-multi/sol6_n20/*/results.tsv, rows 2 to 4 whose description changes only the number of trees or rounds |
