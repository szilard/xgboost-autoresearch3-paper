<!-- analysis/stats.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ c34a051; generated 2026-10-07 20:11Z -->

## Without the 10 caveat runs

| LLM | n | mean | sd | min | p10 | median | p90 | max | 95% CI of the mean (t) | mean improvement over the starter | range | range / improvement | experiments per run | kept per run |
|--------|----|----------|----------|----------|----------|----------|----------|----------|----------------|----------------|----------|----------------|----------------|-------|
| Astra | 17 | 0.6867 | 0.0023 | 0.6815 | 0.6845 | 0.6872 | 0.6888 | 0.6906 | 0.6855 to 0.6879 | +0.0142 | 0.0091 | 0.64 | 46.8 (36 to 62) | 19.1 |
| Sol | 17 | 0.6841 | 0.0015 | 0.6803 | 0.6826 | 0.6841 | 0.6856 | 0.6864 | 0.6833 to 0.6849 | +0.0116 | 0.0061 | 0.53 | 45.0 (29 to 70) | 12.6 |
| Luna | 16 | 0.6807 | 0.0019 | 0.6773 | 0.6789 | 0.6802 | 0.6844 | 0.6844 | 0.6797 to 0.6818 | +0.0082 | 0.0071 | 0.86 | 30.1 (24 to 38) | 8.8 |

## Head to head without the caveat runs

| pair (A vs B) | P(A beats B) | 95% bootstrap interval | mean A − mean B | SE of the difference | difference in SEs | share of tied pairs |
|-------------|-----------|--------------|-----------|---------------|---------------|--------|
| Astra vs Sol | 0.824 (82%) | 0.659 to 0.953 | +0.0026 | 0.0007 | 3.9 | 0.014 |
| Astra vs Luna | 0.971 (97%) | 0.908 to 1.000 | +0.0059 | 0.0007 | 8.1 | 0.000 |
| Sol vs Luna | 0.910 (91%) | 0.790 to 0.996 | +0.0033 | 0.0006 | 5.5 | 0.004 |

## Without the BTS-informed runs (astra6_n20-12, astra6_n20-7, sol6_n20-11)

| LLM | n | mean | sd | min | p10 | median | p90 | max | 95% CI of the mean (t) | mean improvement over the starter | range | range / improvement | experiments per run | kept per run |
|--------|----|----------|----------|----------|----------|----------|----------|----------|----------------|----------------|----------|----------------|----------------|-------|
| Astra | 18 | 0.6864 | 0.0022 | 0.6815 | 0.6845 | 0.6865 | 0.6888 | 0.6906 | 0.6853 to 0.6875 | +0.0139 | 0.0091 | 0.65 | 47.2 (36 to 62) | 18.8 |
| Sol | 19 | 0.6841 | 0.0018 | 0.6803 | 0.6821 | 0.6841 | 0.6864 | 0.6871 | 0.6832 to 0.6850 | +0.0116 | 0.0068 | 0.59 | 44.6 (29 to 70) | 12.8 |
| Luna | 20 | 0.6806 | 0.0019 | 0.6773 | 0.6789 | 0.6800 | 0.6831 | 0.6844 | 0.6798 to 0.6815 | +0.0081 | 0.0071 | 0.87 | 30.1 (24 to 38) | 8.7 |

## Head to head without the BTS-informed runs

| pair (A vs B) | P(A beats B) | 95% bootstrap interval | mean A − mean B | SE of the difference | difference in SEs | share of tied pairs |
|-------------|-----------|--------------|-----------|---------------|---------------|--------|
| Astra vs Sol | 0.791 (79%) | 0.630 to 0.921 | +0.0023 | 0.0007 | 3.4 | 0.020 |
| Astra vs Luna | 0.975 (98%) | 0.922 to 1.000 | +0.0058 | 0.0007 | 8.5 | 0.000 |
| Sol vs Luna | 0.907 (91%) | 0.801 to 0.982 | +0.0034 | 0.0006 | 5.7 | 0.003 |
