<!-- analysis/stats.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ c34a051; generated 2026-10-07 19:37Z -->

## Holdout AUC of the final model, all 60 runs

| LLM | n | mean | sd | min | p10 | median | p90 | max | 95% CI of the mean (t) | mean improvement over the starter | range | range / improvement | experiments per run | kept per run |
|--------|----|----------|----------|----------|----------|----------|----------|----------|----------------|----------------|----------|----------------|----------------|-------|
| Astra | 20 | 0.6866 | 0.0022 | 0.6815 | 0.6845 | 0.6871 | 0.6888 | 0.6906 | 0.6855 to 0.6876 | +0.0141 | 0.0091 | 0.65 | 47.1 (36 to 62) | 19.2 |
| Sol | 20 | 0.6842 | 0.0018 | 0.6803 | 0.6821 | 0.6844 | 0.6864 | 0.6871 | 0.6833 to 0.6850 | +0.0117 | 0.0068 | 0.58 | 45.1 (29 to 70) | 13.0 |
| Luna | 20 | 0.6806 | 0.0019 | 0.6773 | 0.6789 | 0.6800 | 0.6831 | 0.6844 | 0.6798 to 0.6815 | +0.0081 | 0.0071 | 0.87 | 30.1 (24 to 38) | 8.7 |

Starter model: holdout AUC 0.6725. All runs above the starter: True.
sd is the sample standard deviation; p10 and p90 are the nearest runs; the interval uses the t distribution with n − 1 degrees of freedom.

## Overlap of the ranges

- Luna's best run (0.6844) beats 10 of Sol's 20 runs and 2 of Astra's 20.
- Sol's best run (0.6871) beats 10 of Astra's 20 runs.
- Difference between the best and the worst LLM's means: 0.0059.

