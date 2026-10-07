| LLM | first gain, min | holdout at 15 min | 30 min | 45 min | 60 min | experiments | kept | agent's share of the hour | longest plateau, min | runs with a plateau of 20 min or more | steps down per run |
|--------|------|---------|---------|---------|---------|-----------|-------|-------|--------|-------|------|
| Astra | 2.4 | 0.6819 | 0.6836 | 0.6849 | 0.6871 | 47 | 19.2 | 72% | 11 | 2 | 2.2 |
| Sol | 2.9 | 0.6826 | 0.6833 | 0.6837 | 0.6844 | 45 | 13.0 | 54% | 14 | 3 | 1.6 |
| Luna | 5.4 | 0.6784 | 0.6790 | 0.6797 | 0.6800 | 30 | 8.7 | 68% | 20 | 9 | 0.9 |

Table: The hour, per LLM. First gain: median minute of the first kept commit whose holdout AUC exceeds the starter's by more than 0.0005. Holdout at t: median over runs of the holdout AUC of the model kept at minute t. Experiments and kept commits: means per run. Agent's share: time outside XGBoost runs. Plateau: longest interval without a kept commit (median over runs). Steps down: kept commits whose holdout AUC is below the previous kept commit's (mean per run).
