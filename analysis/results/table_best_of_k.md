<!-- analysis/best_of_k.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ c34a051; generated 2026-10-07 17:40Z -->

## Best of k attempts, chosen on eval AUC, holdout AUC of the chosen run (exact over the 20 observed runs per LLM)

| LLM | k | median | mean | 5th percentile | 95th percentile | oracle (chosen on holdout) median | oracle mean − chosen mean |
|--------|----|--------------------------------------------------|----------|---------------|---------------|------------|-----------|
| Astra | 1 | 0.6871 | 0.6866 | 0.6815 | 0.6888 | 0.6871 | +0.0000 |
| Astra | 2 | 0.6878 | 0.6877 | 0.6846 | 0.6906 | 0.6880 | +0.0001 |
| Astra | 3 | 0.6881 | 0.6882 | 0.6856 | 0.6906 | 0.6881 | +0.0001 |
| Astra | 5 | 0.6886 | 0.6887 | 0.6872 | 0.6906 | 0.6888 | +0.0001 |
| Astra | 10 | 0.6888 | 0.6893 | 0.6876 | 0.6906 | 0.6888 | +0.0001 |
| Astra |  | Spearman(eval, holdout) = 0.94 |  |  |  |  |  |
| Astra |  | median gain over k = 1: k = 2: +0.0007, k = 3: +0.0010, k = 5: +0.0015, k = 10: +0.0017 |  |  |  |  |  |
| Astra |  | oracle median minus eval-chosen median: k = 1: +0.0000, k = 2: +0.0002, k = 3: +0.0000, k = 5: +0.0002, k = 10: +0.0000 |  |  |  |  |  |
| Sol | 1 | 0.6844 | 0.6842 | 0.6803 | 0.6866 | 0.6844 | -0.0000 |
| Sol | 2 | 0.6854 | 0.6851 | 0.6834 | 0.6871 | 0.6854 | +0.0001 |
| Sol | 3 | 0.6856 | 0.6855 | 0.6837 | 0.6871 | 0.6856 | +0.0001 |
| Sol | 5 | 0.6857 | 0.6858 | 0.6838 | 0.6871 | 0.6864 | +0.0003 |
| Sol | 10 | 0.6857 | 0.6860 | 0.6854 | 0.6871 | 0.6866 | +0.0005 |
| Sol |  | Spearman(eval, holdout) = 0.91 |  |  |  |  |  |
| Sol |  | median gain over k = 1: k = 2: +0.0010, k = 3: +0.0012, k = 5: +0.0013, k = 10: +0.0013 |  |  |  |  |  |
| Sol |  | oracle median minus eval-chosen median: k = 1: +0.0000, k = 2: +0.0000, k = 3: +0.0000, k = 5: +0.0007, k = 10: +0.0009 |  |  |  |  |  |
| Luna | 1 | 0.6800 | 0.6807 | 0.6773 | 0.6844 | 0.6800 | -0.0000 |
| Luna | 2 | 0.6818 | 0.6816 | 0.6795 | 0.6844 | 0.6819 | +0.0000 |
| Luna | 3 | 0.6820 | 0.6822 | 0.6797 | 0.6844 | 0.6820 | +0.0000 |
| Luna | 5 | 0.6831 | 0.6829 | 0.6800 | 0.6844 | 0.6831 | +0.0000 |
| Luna | 10 | 0.6844 | 0.6837 | 0.6817 | 0.6844 | 0.6844 | +0.0000 |
| Luna |  | Spearman(eval, holdout) = 0.96 |  |  |  |  |  |
| Luna |  | median gain over k = 1: k = 2: +0.0018, k = 3: +0.0020, k = 5: +0.0031, k = 10: +0.0044 |  |  |  |  |  |
| Luna |  | oracle median minus eval-chosen median: k = 1: +0.0000, k = 2: +0.0001, k = 3: +0.0000, k = 5: +0.0000, k = 10: +0.0000 |  |  |  |  |  |

Draws are with replacement from the observed runs, so the ceiling is the best observed run. The oracle picks on holdout AUC and shows how little is lost by picking on eval AUC. Post hoc: the policy was defined after the runs.

## Simulation check (20,000 draws, seed 1)

| LLM | k | median | mean |
|--------|----|----------|----------|
| Astra | 1 | 0.6872 | 0.6866 |
| Astra | 2 | 0.6878 | 0.6877 |
| Astra | 3 | 0.6881 | 0.6882 |
| Astra | 5 | 0.6886 | 0.6887 |
| Astra | 10 | 0.6888 | 0.6893 |
| Sol | 1 | 0.6841 | 0.6842 |
| Sol | 2 | 0.6854 | 0.6851 |
| Sol | 3 | 0.6856 | 0.6855 |
| Sol | 5 | 0.6857 | 0.6858 |
| Sol | 10 | 0.6857 | 0.6860 |
| Luna | 1 | 0.6800 | 0.6807 |
| Luna | 2 | 0.6819 | 0.6816 |
| Luna | 3 | 0.6820 | 0.6822 |
| Luna | 5 | 0.6831 | 0.6829 |
| Luna | 10 | 0.6844 | 0.6837 |
