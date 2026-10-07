#!/usr/bin/env python3
"""Per-LLM statistics, head-to-head win probabilities, tests, runs-per-arm, sensitivity."""
import itertools
import numpy as np
from scipy import stats as ss
from common import BASE_HOLDOUT, BTS_INFORMED, MODELS, SHORT, by_model, f4, load_runs, md_table, runs_repo, write

N_BOOT, SEED = 10000, 1
repo = runs_repo()
runs = load_runs(repo, with_session=False)


def per_model_table(rs, title):
    rows = []
    for m in MODELS:
        x = np.array([r["holdout_auc"] for r in rs if r["model"] == m]); n = len(x)
        if n == 0:
            continue
        sd = x.std(ddof=1); half = ss.t.ppf(0.975, n - 1) * sd / np.sqrt(n)
        p10, p90 = np.percentile(x, [10, 90], method="nearest")
        ex = [r["experiments"] for r in rs if r["model"] == m]; nk = [r["n_keep"] for r in rs if r["model"] == m]
        rows.append([SHORT[m], n, f4(x.mean()), f4(sd), f4(x.min()), f4(p10), f4(np.median(x)), f4(p90), f4(x.max()),
                     f"{x.mean()-half:.4f} to {x.mean()+half:.4f}", f"{x.mean()-BASE_HOLDOUT:+.4f}",
                     f4(x.max() - x.min()), f"{(x.max()-x.min())/(x.mean()-BASE_HOLDOUT):.2f}",
                     f"{np.mean(ex):.1f} ({min(ex)} to {max(ex)})", f"{np.mean(nk):.1f}"])
    t = f"## {title}\n\n" + md_table(["LLM", "n", "mean", "sd", "min", "p10", "median", "p90", "max", "95% CI of the mean (t)",
                                      "mean improvement over the starter", "range", "range / improvement",
                                      "experiments per run", "kept per run"], rows)
    return t


def pairwise_table(rs, title, rng):
    d = {m: np.array([r["holdout_auc"] for r in rs if r["model"] == m]) for m in MODELS}
    rows = []
    for a, b in itertools.combinations(MODELS, 2):
        A, B = d[a], d[b]
        win = (A[:, None] > B[None, :]) + 0.5 * (A[:, None] == B[None, :]); p = win.mean()
        ia = rng.integers(0, len(A), (N_BOOT, len(A))); ib = rng.integers(0, len(B), (N_BOOT, len(B)))
        boot = win[ia[:, :, None], ib[:, None, :]].mean(axis=(1, 2)); lo, hi = np.percentile(boot, [2.5, 97.5])
        diff = A.mean() - B.mean(); se = np.sqrt(A.var(ddof=1) / len(A) + B.var(ddof=1) / len(B))
        rows.append([f"{SHORT[a]} vs {SHORT[b]}", f"{p:.3f} ({p:.0%})", f"{lo:.3f} to {hi:.3f}", f"{diff:+.4f}",
                     f"{se:.4f}", f"{diff/se:.1f}", f"{(A[:, None] == B[None, :]).mean():.3f}"])
    return f"## {title}\n\n" + md_table(["pair (A vs B)", "P(A beats B)", "95% bootstrap interval", "mean A − mean B",
                                         "SE of the difference", "difference in SEs", "share of tied pairs"], rows)


rng = np.random.default_rng(SEED)
out = per_model_table(runs, "Holdout AUC of the final model, all 60 runs")
out += f"\nStarter model: holdout AUC {BASE_HOLDOUT}. All runs above the starter: {all(r['holdout_auc'] > BASE_HOLDOUT for r in runs)}.\n"
out += "sd is the sample standard deviation; p10 and p90 are the nearest runs; the interval uses the t distribution with n − 1 degrees of freedom.\n\n"
hm = by_model(runs)
L, S, A = (np.array(hm[m]) for m in ("gpt-6-luna", "gpt-6-sol", "gpt-6-astra"))
out += ("## Overlap of the ranges\n\n"
        f"- Luna's best run ({L.max():.4f}) beats {(S < L.max()).sum()} of Sol's 20 runs and {(A < L.max()).sum()} of Astra's 20.\n"
        f"- Sol's best run ({S.max():.4f}) beats {(A < S.max()).sum()} of Astra's 20 runs.\n"
        f"- Difference between the best and the worst LLM's means: {A.mean()-L.mean():.4f}.\n\n")
write("table_per_model.md", out, repo)

write("table_pairwise.md", pairwise_table(runs, "Head to head, all 60 runs", rng)
      + "\nP(A beats B): share of the 400 (run of A, run of B) pairs in which A's holdout AUC is higher, ties counted half "
      "(Mann–Whitney probability of superiority, Vargha–Delaney A). Bootstrap: runs resampled with replacement within "
      f"each LLM, {N_BOOT} resamples, seed {SEED}.\n", repo)

# tests (appendix)
rows = []
for a, b in itertools.combinations(MODELS, 2):
    A_, B_ = np.array(hm[a]), np.array(hm[b])
    t = ss.ttest_ind(A_, B_, equal_var=False); u = ss.mannwhitneyu(A_, B_, alternative="two-sided")
    rows.append([f"{SHORT[a]} vs {SHORT[b]}", f"{t.statistic:.2f}", f"{t.pvalue:.1e}", f"{u.statistic:.0f}", f"{u.pvalue:.1e}"])
f = ss.f_oneway(*[hm[m] for m in MODELS]); kw = ss.kruskal(*[hm[m] for m in MODELS])
write("tests.md", "## Pairwise tests (two-sided)\n\n" + md_table(["pair", "Welch t", "p", "Mann–Whitney U", "p"], rows)
      + f"\nOne-way ANOVA over the three LLMs: F = {f.statistic:.1f}, p = {f.pvalue:.1e}. Kruskal–Wallis: H = {kw.statistic:.1f}, p = {kw.pvalue:.1e}.\n", repo)

# runs per arm (post hoc illustration)
rows = []
for a, b in itertools.combinations(MODELS, 2):
    A_, B_ = np.array(hm[a]), np.array(hm[b]); gap = abs(A_.mean() - B_.mean())
    sd = np.sqrt((A_.var(ddof=1) + B_.var(ddof=1)) / 2)
    rows.append([f"{SHORT[a]} vs {SHORT[b]}", f4(gap), f4(sd), f"{16*sd**2/gap**2:.0f}"])
write("table_runs_per_arm.md", "## Runs per arm to detect the observed gap (post hoc illustration)\n\n"
      + md_table(["pair", "observed gap of means", "pooled sd", "runs per arm (16 sd² / gap²)"], rows)
      + "\nThe approximation 16 sd² / gap² gives the runs per arm for 80% power in a two-sided test at the 5% level. "
      "The gaps were observed, not fixed in advance, so these counts illustrate the scale and are not a design rule.\n", repo)

# sensitivity
rng2 = np.random.default_rng(SEED)
no_cav = [r for r in runs if r["valid"] == "yes"]
no_bts = [r for r in runs if r["run"] not in BTS_INFORMED]
s = per_model_table(no_cav, f"Without the {len(runs)-len(no_cav)} caveat runs") + "\n" + pairwise_table(no_cav, "Head to head without the caveat runs", rng2)
s += "\n" + per_model_table(no_bts, f"Without the BTS-informed runs ({', '.join(sorted(BTS_INFORMED))})") + "\n" + pairwise_table(no_bts, "Head to head without the BTS-informed runs", rng2)
write("sensitivity.md", s, repo)
