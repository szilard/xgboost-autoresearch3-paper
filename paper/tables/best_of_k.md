| LLM | k = 1 | k = 2 | k = 3 | k = 5 | k = 10 | k = 3, 5th percentile | k = 3, chosen on holdout |
|--------|----------|----------|----------|----------|----------|---------------|-----------|
| Astra | 0.6871 | 0.6878 | 0.6881 | 0.6886 | 0.6888 | 0.6856 | 0.6881 |
| Sol | 0.6844 | 0.6854 | 0.6856 | 0.6857 | 0.6857 | 0.6837 | 0.6856 |
| Luna | 0.6800 | 0.6818 | 0.6820 | 0.6831 | 0.6844 | 0.6797 | 0.6820 |

Table: Running the agent k times and choosing the run with the best eval AUC: median holdout AUC of the chosen run, computed exactly over the 20 observed runs with draws with replacement (for k = 1, the median of Table 2). The last two columns give, for k = 3, the 5th percentile of the chosen run's holdout AUC, from the same exact distribution, and the median if the choice were made on the holdout set itself.
