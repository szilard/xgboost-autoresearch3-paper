<!-- analysis/stats.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ c34a051; generated 2026-10-07 20:11Z -->

## Head to head, all 60 runs

| pair (A vs B) | P(A beats B) | 95% bootstrap interval | mean A − mean B | SE of the difference | difference in SEs | share of tied pairs |
|-------------|-----------|--------------|-----------|---------------|---------------|--------|
| Astra vs Sol | 0.801 (80%) | 0.656 to 0.925 | +0.0024 | 0.0006 | 3.7 | 0.018 |
| Astra vs Luna | 0.978 (98%) | 0.927 to 1.000 | +0.0059 | 0.0006 | 9.2 | 0.000 |
| Sol vs Luna | 0.911 (91%) | 0.810 to 0.983 | +0.0035 | 0.0006 | 6.0 | 0.003 |

P(A beats B): share of the 400 (run of A, run of B) pairs in which A's holdout AUC is higher, ties counted half (Mann–Whitney probability of superiority, Vargha–Delaney A). Bootstrap: runs resampled with replacement within each LLM, 10000 resamples, seed 1.
