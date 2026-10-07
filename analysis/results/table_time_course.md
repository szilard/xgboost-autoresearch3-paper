<!-- analysis/time_course.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ c34a051; generated 2026-10-07 21:21Z -->

## Time course per LLM

| LLM | first holdout gain, min (mean / median) | median holdout at 15 min | 30 min | 45 min | 60 min (final) | experiments per run | kept | discarded | crashed | AI share of the hour | longest plateau, min (median) | runs with a plateau ≥ 20 min | steps down on holdout per run | runs whose final model is below their best kept model on holdout | minutes to within 0.002 of the final (median) |
|--------|-----------|-----------|----------|----------|-----------|----------------|-------|--------------|-----------|--------|---------------|-----------|-----------|-----------|------------|
| Astra | 2.9 / 2.4 | 0.6819 | 0.6836 | 0.6849 | 0.6871 | 47.1 | 19.2 | 27.6 | 0.25 | 71.5% | 10.7 (max 26.1) | 2 | 2.25 | 4 | 34.9 |
| Sol | 3.3 / 2.9 | 0.6826 | 0.6833 | 0.6837 | 0.6844 | 45.1 | 13.0 | 31.8 | 0.30 | 53.6% | 14.2 (max 41.0) | 3 | 1.55 | 6 | 15.2 |
| Luna | 5.8 / 5.4 | 0.6784 | 0.6790 | 0.6797 | 0.6800 | 30.1 | 8.7 | 21.0 | 0.35 | 67.7% | 19.6 (max 50.6) | 9 | 0.90 | 3 | 14.6 |

First holdout gain: first kept commit whose holdout AUC exceeds the starter's by more than 0.0005. Holdout at t: the holdout AUC of the model kept at minute t (starter until the first keep); the table gives the median over the LLM's runs. Plateau: longest interval between consecutive kept commits (or until the clock stopped). Steps down: kept commits whose holdout AUC is below the previous kept commit's. AI share: time outside harness runs, from the harness report.

## The first kept improvement (first kept commit with a higher eval AUC than the baseline)

| LLM | runs | minute (median) | holdout AUC after it (median) | (mean) | mentions depth/leaves | mentions learning rate | mentions trees/rounds | mentions calendar | runs with a kept depth/leaves change | its minute (median) | holdout AUC after the first kept depth/leaves change (median) |
|--------|-------|------------|------------|----------|------------------|------------|------------------|------------|------------------|------------|------------------|
| Astra | 20 | 2.4 | 0.6766 | 0.6766 | 12 | 7 | 15 | 5 | 19 | 3.4 | 0.6784 |
| Sol | 20 | 2.6 | 0.6775 | 0.6762 | 11 | 7 | 11 | 2 | 19 | 3.2 | 0.6779 |
| Luna | 20 | 5.4 | 0.6760 | 0.6754 | 8 | 2 | 2 | 0 | 17 | 8.6 | 0.6773 |

The mention counts are regular-expression matches on the agent's own one-line description of the commit (heuristic).
