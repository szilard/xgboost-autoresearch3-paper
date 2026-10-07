<!-- analysis/stats.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ b2841ab; generated 2026-10-07 16:11Z -->

## Runs per arm to detect the observed gap (post hoc illustration)

| pair | observed gap of means | pooled sd | runs per arm (16 sd² / gap²) |
|-------------|------------|-----------|--------|
| Astra vs Sol | 0.0024 | 0.0020 | 11 |
| Astra vs Luna | 0.0059 | 0.0020 | 2 |
| Sol vs Luna | 0.0035 | 0.0019 | 4 |

The approximation 16 sd² / gap² gives the runs per arm for 80% power in a two-sided test at the 5% level. The gaps were observed, not fixed in advance, so these counts illustrate the scale and are not a design rule.
