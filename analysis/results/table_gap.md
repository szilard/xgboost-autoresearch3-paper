<!-- analysis/gap.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ b2841ab; generated 2026-10-07 16:11Z -->

## Eval and holdout AUC of the final models

| LLM | mean eval AUC | mean holdout AUC | mean gap (holdout − eval) | sd | min | max | Spearman(eval, holdout) | Spearman(kept commits, gap) | Spearman(experiments, holdout) | Spearman(kept commits, holdout) |
|---------|-----------|-----------|------------|-----------|------------|------------|--------------------|-------------------|------------------------------|-------------------|
| Astra | 0.6893 | 0.6866 | -0.0028 | 0.0005 | -0.0037 | -0.0019 | 0.94 | -0.29 | +0.40 | +0.67 |
| Sol | 0.6860 | 0.6842 | -0.0018 | 0.0007 | -0.0036 | -0.0006 | 0.91 | -0.24 | +0.45 | +0.38 |
| Luna | 0.6825 | 0.6806 | -0.0018 | 0.0006 | -0.0032 | -0.0006 | 0.96 | +0.39 | +0.36 | +0.64 |

Starter: eval 0.6743, holdout 0.6725, gap -0.0018. Eval and holdout are disjoint halves of one balanced 2006 sample of 100,000 flights; with 25,000 per class the standard error of one AUC near 0.68 is about 0.002 (Hanley and McNeil). The correlations with kept commits and experiments are exploratory.
