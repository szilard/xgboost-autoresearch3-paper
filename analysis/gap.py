#!/usr/bin/env python3
"""Eval–holdout gap of the final models, and how eval and holdout AUC rank the runs."""
import numpy as np
from scipy import stats as ss
from common import BASE_EVAL, BASE_HOLDOUT, MODELS, SHORT, load_runs, md_table, runs_repo, write

repo = runs_repo()
runs = load_runs(repo, with_session=False)
rows = []
for m in MODELS:
    rr = [r for r in runs if r["model"] == m]
    g = np.array([r["gap"] for r in rr]); e = np.array([r["best_eval_auc"] for r in rr]); h = np.array([r["holdout_auc"] for r in rr])
    nk = np.array([r["n_keep"] for r in rr]); ex = np.array([r["experiments"] for r in rr])
    rows.append([SHORT[m], f"{e.mean():.4f}", f"{h.mean():.4f}", f"{g.mean():+.4f}", f"{g.std(ddof=1):.4f}", f"{g.min():+.4f}", f"{g.max():+.4f}",
                 f"{ss.spearmanr(e, h).correlation:.2f}", f"{ss.spearmanr(nk, g).correlation:+.2f}", f"{ss.spearmanr(ex, h).correlation:+.2f}",
                 f"{ss.spearmanr(nk, h).correlation:+.2f}"])
out = "## Eval and holdout AUC of the final models\n\n" + md_table(
    ["LLM", "mean eval AUC", "mean holdout AUC", "mean gap (holdout − eval)", "sd", "min", "max", "Spearman(eval, holdout)",
     "Spearman(kept commits, gap)", "Spearman(experiments, holdout)", "Spearman(kept commits, holdout)"], rows)
out += (f"\nStarter: eval {BASE_EVAL}, holdout {BASE_HOLDOUT}, gap {BASE_HOLDOUT-BASE_EVAL:+.4f}. Eval and holdout are disjoint halves of one "
        "balanced 2006 sample of 100,000 flights; with 25,000 per class the standard error of one AUC near 0.68 is about 0.002 "
        "(Hanley and McNeil). The correlations with kept commits and experiments are exploratory.\n")
write("table_gap.md", out, repo)
