#!/usr/bin/env python3
"""Figures for the paper, as PDF and PNG in figures/.

F1–F4 reuse the runs repo's own plotting tools (tools/plot_holdout_auc.py, tools/pairwise_win_prob.py)
with their output redirected here; F5–F9 are new, in the same style.
"""
import csv
import sys
import importlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from common import BASE_EVAL, BASE_HOLDOUT, COLOUR, FIGURES, MODELS, RESULTS, SHORT, load_runs, runs_repo

plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 10})
repo = runs_repo()
FIGURES.mkdir(exist_ok=True)
sys.path.insert(0, str(repo / "tools"))
pha = importlib.import_module("plot_holdout_auc")
pwp = importlib.import_module("pairwise_win_prob")


def save_both(fig, name):
    stem = name.rsplit(".", 1)[0]
    for ext in ("pdf", "png"):
        out = FIGURES / f"{stem}.{ext}"
        fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=pha.SURFACE)
        print(out.relative_to(FIGURES.parent))
    plt.close(fig)


# the runs repo's tools say "model" for an LLM; the paper keeps "model" for the XGBoost model
RELABEL = [("one run of each model", "one run of each LLM"), ("right-hand model wins", "right-hand LLM wins"),
           ("resampled per model", "resampled per LLM"), ("one panel per model", "one panel per LLM"),
           ("other models' runs", "other LLMs' runs"), (" (n >= 5)", "")]


def save_relabelled(fig, name):
    for t in fig.findobj(matplotlib.text.Text):
        s = t.get_text()
        for a, b in RELABEL:
            s = s.replace(a, b)
        t.set_text(s)
    save_both(fig, name)


pha.RUN_MULTI = repo / "run-multi"; pha.OUT_DIR = FIGURES; pha.save = save_relabelled
pwp.RUN_MULTI = pha.RUN_MULTI; pwp.save = save_relabelled
# F1, F3, F4
pha.main()
# F2 (the tool prints its table too)
pwp.main()

runs = load_runs(repo, with_session=False)
SURFACE, INK, INK2, GRID = pha.SURFACE, pha.INK, pha.INK2, pha.GRID


def style(ax, title):
    pha.style(ax, title); ax.grid(color=GRID, lw=0.8)


# F5: eval vs holdout
fig, ax = plt.subplots(figsize=(6.2, 5.2), facecolor=SURFACE)
lo = min(min(r["best_eval_auc"], r["holdout_auc"]) for r in runs) - 0.001; hi = max(max(r["best_eval_auc"], r["holdout_auc"]) for r in runs) + 0.001
ax.plot([lo, hi], [lo, hi], color=INK2, lw=1, ls=(0, (3, 3)), zorder=1)
ax.plot([lo, hi], [lo + BASE_HOLDOUT - BASE_EVAL, hi + BASE_HOLDOUT - BASE_EVAL], color=INK2, lw=0.8, ls=(0, (1, 2)), zorder=1)
for m in MODELS:
    rr = [r for r in runs if r["model"] == m]
    ax.scatter([r["best_eval_auc"] for r in rr], [r["holdout_auc"] for r in rr], s=40, color=COLOUR[m], label=m, zorder=3, edgecolors=SURFACE, linewidths=0.6)
ax.set_xlabel("eval AUC of the final model", color=INK2); ax.set_ylabel("holdout AUC of the final model", color=INK2)
ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal")
style(ax, "Eval against holdout AUC, one dot per run")
ax.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="upper left")
ax.text(hi - 0.0012, hi - 0.0012, "equal", color=INK2, fontsize=8, ha="right", va="bottom", rotation=45)
ax.text(hi - 0.0004, hi + BASE_HOLDOUT - BASE_EVAL - 0.0010, "starter's gap", color=INK2, fontsize=8, ha="right", va="top", rotation=45)
save_both(fig, "eval_vs_holdout.png")

# F6: best of k curves (exact, as in best_of_k.py)
from best_of_k import dist, quantile  # noqa: E402  (importing runs that script's main; cheap)
fig, ax = plt.subplots(figsize=(6.8, 4.4), facecolor=SURFACE)
ks = list(range(1, 11))
for m in MODELS:
    rr = [r for r in runs if r["model"] == m]
    e = np.array([r["best_eval_auc"] for r in rr]); h = np.array([r["holdout_auc"] for r in rr])
    med = [quantile(dist(e, h, k), 0.5) for k in ks]; p5 = [quantile(dist(e, h, k), 0.05) for k in ks]; p95 = [quantile(dist(e, h, k), 0.95) for k in ks]
    om = [quantile(dist(h, h, k), 0.5) for k in ks]
    ax.fill_between(ks, p5, p95, color=COLOUR[m], alpha=0.12, lw=0)
    ax.plot(ks, med, color=COLOUR[m], lw=2.2, marker="o", ms=4, label=m)
    ax.plot(ks, om, color=COLOUR[m], lw=1, ls=(0, (3, 2)))
ax.set_xlabel("number of runs k (best eval AUC kept)", color=INK2); ax.set_ylabel("holdout AUC of the kept run", color=INK2)
ax.set_xticks(ks)
style(ax, "Best of k runs: median (line), 5th to 95th percentile (band), oracle on holdout (dashed)")
ax.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="lower right")
save_both(fig, "best_of_k.png")

# F7: feature audit bars
rows = list(csv.DictReader(open(RESULTS / "feature_audit_per_run.csv")))
cats = [("dom_cat", "DayofMonth kept\nas a category"), ("doy", "day-of-year-like\nnumeric feature"), ("holiday", "holiday\nfeatures")]
fig, ax = plt.subplots(figsize=(6.8, 3.6), facecolor=SURFACE)
w = 0.26
for i, m in enumerate(MODELS):
    rr = [x for x in rows if x["model"] == m]
    vals = [sum(int(x[c]) for x in rr) / len(rr) for c, _ in cats]
    ax.bar(np.arange(len(cats)) + (i - 1) * w, vals, w, color=COLOUR[m], label=m)
    for j, v in enumerate(vals):
        ax.text(j + (i - 1) * w, v + 0.02, f"{int(round(v*len(rr)))}", ha="center", va="bottom", fontsize=8, color=INK2)
ax.set_xticks(range(len(cats))); ax.set_xticklabels([l for _, l in cats], color=INK)
ax.set_ylim(0, 1.08); ax.set_ylabel("share of the 20 final models", color=INK2)
style(ax, "How the final models handle the calendar (heuristic audit, provisional)")
ax.grid(axis="x", visible=False)
ax.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="upper right")
save_both(fig, "feature_audit.png")

# F8: example run astra6_n20-1
ex = next(r for r in runs if r["run"] == "astra6_n20-1")
fig, ax = plt.subplots(figsize=(7.5, 4.2), facecolor=SURFACE)
t = [m_ for m_, *_ in ex["path"]]; h = [x[1] for x in ex["path"]]; e = [x[2] for x in ex["path"]]
ax.step(t + [ex["end_min"]], e + [e[-1]], where="post", color=INK2, lw=1.4, label="eval AUC (what the agent sees)")
ax.step(t + [ex["end_min"]], h + [h[-1]], where="post", color=COLOUR[ex["model"]], lw=2.2, label="holdout AUC (scored afterwards)")
ax.scatter(t, e, s=14, color=INK2, zorder=3); ax.scatter(t, h, s=18, color=COLOUR[ex["model"]], zorder=3)
ax.set_xlabel("minutes since the clock started", color=INK2); ax.set_ylabel("AUC", color=INK2); ax.set_xlim(0, 61)
style(ax, f"One run in detail: {ex['run']}, {len(ex['path'])} kept commits of {ex['experiments']} experiments")
ax.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="lower right")
save_both(fig, "example_run.png")

# F9: experiments vs holdout
fig, ax = plt.subplots(figsize=(6.2, 4.2), facecolor=SURFACE)
for m in MODELS:
    rr = [r for r in runs if r["model"] == m]
    ax.scatter([r["experiments"] for r in rr], [r["holdout_auc"] for r in rr], s=40, color=COLOUR[m], label=m, edgecolors=SURFACE, linewidths=0.6, zorder=3)
ax.set_xlabel("experiments in the hour (rows of results.tsv)", color=INK2); ax.set_ylabel("holdout AUC of the final model", color=INK2)
style(ax, "Experiments per run against holdout AUC")
ax.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="lower right")
save_both(fig, "experiments_vs_holdout.png")
