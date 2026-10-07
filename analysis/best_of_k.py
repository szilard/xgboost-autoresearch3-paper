#!/usr/bin/env python3
"""Best of k: run the agent k times, keep the run with the best eval AUC, report its holdout AUC.

Exact over the observed runs: k draws with replacement from a LLM's 20 runs; the run of eval rank
r (ascending) is the best of the k with probability (R_hi/n)^k − (R_lo/n)^k for its tie group,
shared equally within the group. Median and 5th/95th percentiles of the chosen run's holdout AUC
follow from that distribution. An oracle chooses on holdout AUC instead. A simulation checks the
exact figures.
"""
import numpy as np
from scipy import stats as ss
from common import MODELS, SHORT, load_runs, md_table, runs_repo, write

KS = (1, 2, 3, 5, 10)


def dist(score, holdout, k):
    """{holdout value: probability} of the holdout of the run chosen by max score among k draws."""
    n = len(score); order = np.argsort(score, kind="stable"); s = score[order]; h = holdout[order]
    p = np.zeros(n); i = 0
    while i < n:
        j = i
        while j + 1 < n and s[j + 1] == s[i]:
            j += 1
        mass = ((j + 1) / n) ** k - (i / n) ** k
        p[i:j + 1] = mass / (j - i + 1); i = j + 1
    d = {}
    for hv, pv in zip(h, p):
        d[hv] = d.get(hv, 0) + pv
    return d


def quantile(d, q):
    c = 0
    for hv in sorted(d):
        c += d[hv]
        if c >= q - 1e-12:
            return hv



def main():
    repo = runs_repo()
    runs = load_runs(repo, with_session=False)
    rows, sim_rows = [], []
    rng = np.random.default_rng(1)
    for m in MODELS:
        rr = [r for r in runs if r["model"] == m]
        e = np.array([r["best_eval_auc"] for r in rr]); h = np.array([r["holdout_auc"] for r in rr])
        for k in KS:
            d = dist(e, h, k); o = dist(h, h, k)
            mean = sum(hv * pv for hv, pv in d.items()); omean = sum(hv * pv for hv, pv in o.items())
            idx = rng.integers(0, len(rr), (20000, k)); pick = idx[np.arange(20000), e[idx].argmax(axis=1)]; hs = h[pick]
            rows.append([SHORT[m], k, f"{quantile(d, 0.5):.4f}", f"{mean:.4f}", f"{quantile(d, 0.05):.4f}", f"{quantile(d, 0.95):.4f}",
                         f"{quantile(o, 0.5):.4f}", f"{omean - mean:+.4f}"])
            sim_rows.append([SHORT[m], k, f"{np.median(hs):.4f}", f"{hs.mean():.4f}"])
        rho = ss.spearmanr(e, h).correlation
        rows.append([SHORT[m], "", f"Spearman(eval, holdout) = {rho:.2f}", "", "", "", "", ""])
        g = {k: quantile(dist(e, h, k), 0.5) - quantile(dist(e, h, 1), 0.5) for k in KS}
        rows.append([SHORT[m], "", "median gain over k = 1: " + ", ".join(f"k = {k}: {g[k]:+.4f}" for k in KS if k > 1), "", "", "", "", ""])
    out = "## Best of k attempts, chosen on eval AUC, holdout AUC of the chosen run (exact over the 20 observed runs per LLM)\n\n"
    out += md_table(["LLM", "k", "median", "mean", "5th percentile", "95th percentile", "oracle (chosen on holdout) median", "oracle mean − chosen mean"], rows)
    out += ("\nDraws are with replacement from the observed runs, so the ceiling is the best observed run. The oracle picks on holdout "
            "AUC and shows how little is lost by picking on eval AUC. Post hoc: the policy was defined after the runs.\n\n"
            "## Simulation check (20,000 draws, seed 1)\n\n" + md_table(["LLM", "k", "median", "mean"], sim_rows))
    write("table_best_of_k.md", out, repo)


if __name__ == "__main__":
    main()
