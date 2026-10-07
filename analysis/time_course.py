#!/usr/bin/env python3
"""Time course of each run: first gain, holdout at 15/30/45/60 min, plateaus, steps down, first move."""
import csv
import re
import statistics as st
import numpy as np
from common import BASE_HOLDOUT, MODELS, PAPER_ROOT, RESULTS, SHORT, load_runs, md_table, runs_repo, write

repo = runs_repo()
runs = load_runs(repo, with_session=False)
GAIN = 0.0005


def course(r):
    path, end = r["path"], r["end_min"]
    def at(t):
        v = [h for m, h, _, _ in path if m <= t]; return v[-1] if v else BASE_HOLDOUT
    first = next((m for m, h, _, _ in path if h > BASE_HOLDOUT + GAIN), None)
    final = path[-1][1]
    near = next((m for m, h, _, _ in path if h >= final - 0.002), None)
    times = [m for m, *_ in path] + [end]
    plateau = max(b - a for a, b in zip(times, times[1:]))
    downs = sum(1 for (_, h1, _, _), (_, h2, _, _) in zip(path, path[1:]) if h2 < h1)
    # the first kept change that raised the eval AUC above the baseline's
    base_eval = path[0][2]
    fk = next(((m, h, e, d) for m, h, e, d in path[1:] if e > base_eval), None)
    fd = next(((m, h, e, d) for m, h, e, d in path[1:] if e > base_eval and re.search(r"depth|leaves|shallow", d.lower())), None)
    return dict(first_depth=fd, first=first, h15=at(15), h30=at(30), h45=at(45), h60=at(60), final=final, near=near, plateau=plateau,
                downs=downs, first_keep=fk)


C = {r["run"]: course(r) for r in runs}
rows, per_run = [], []
for m in MODELS:
    cs = [C[r["run"]] for r in runs if r["model"] == m]
    rr = [r for r in runs if r["model"] == m]
    med = lambda k: st.median([c[k] for c in cs if c[k] is not None])
    mean = lambda k: st.mean([c[k] for c in cs if c[k] is not None])
    rows.append([SHORT[m], f"{mean('first'):.1f} / {med('first'):.1f}", f"{med('h15'):.4f}", f"{med('h30'):.4f}", f"{med('h45'):.4f}",
                 f"{med('h60'):.4f}", f"{st.mean(r['experiments'] for r in rr):.1f}", f"{st.mean(r['n_keep'] for r in rr):.1f}",
                 f"{st.mean(r['n_discard'] for r in rr):.1f}", f"{st.mean(r['n_crash'] for r in rr):.2f}",
                 f"{st.mean(r['ai_share_pct'] for r in rr):.1f}%", f"{med('plateau'):.1f} (max {max(c['plateau'] for c in cs):.1f})",
                 sum(c["plateau"] >= 20 for c in cs), f"{mean('downs'):.2f}", sum(r["final_below_best"] for r in rr), f"{med('near'):.1f}"])
out = "## Time course per LLM\n\n" + md_table(
    ["LLM", "first holdout gain, min (mean / median)", "median holdout at 15 min", "30 min", "45 min", "60 min (final)",
     "experiments per run", "kept", "discarded", "crashed", "AI share of the hour", "longest plateau, min (median)",
     "runs with a plateau ≥ 20 min", "steps down on holdout per run", "runs whose final model is below their best kept model on holdout",
     "minutes to within 0.002 of the final (median)"], rows)
out += (f"\nFirst holdout gain: first kept commit whose holdout AUC exceeds the starter's by more than {GAIN}. "
        "Holdout at t: the holdout AUC of the model kept at minute t (starter until the first keep); the table gives the median over the LLM's runs. "
        "Plateau: longest interval between consecutive kept commits (or until the clock stopped). "
        "Steps down: kept commits whose holdout AUC is below the previous kept commit's. AI share: time outside harness runs, from the harness report.\n")

# first kept improvement
rows = []
for m in MODELS:
    fks = [C[r["run"]]["first_keep"] for r in runs if r["model"] == m]
    fks = [x for x in fks if x]
    desc = " ".join(d.lower() for *_, d in fks)
    depth = sum(bool(re.search(r"depth|leaves|shallow", d.lower())) for *_, d in fks)
    lr = sum(bool(re.search(r"learning.rate|\beta\b|\blr\b|shrink", d.lower())) for *_, d in fks)
    trees = sum(bool(re.search(r"tree|estimator|round", d.lower())) for *_, d in fks)
    cal = sum(bool(re.search(r"dayofmonth|day.of.month|month|calendar|day.of.year|doy", d.lower())) for *_, d in fks)
    fds = [C[r["run"]]["first_depth"] for r in runs if r["model"] == m]; fds = [x for x in fds if x]
    rows.append([SHORT[m], len(fks), f"{st.median(m_ for m_, *_ in fks):.1f}", f"{st.median(h for _, h, *_ in fks):.4f}",
                 f"{st.mean(h for _, h, *_ in fks):.4f}", depth, lr, trees, cal, len(fds),
                 f"{st.median(m_ for m_, *_ in fds):.1f}", f"{st.median(h for _, h, *_ in fds):.4f}"])
out += "\n## The first kept improvement (first kept commit with a higher eval AUC than the baseline)\n\n" + md_table(
    ["LLM", "runs", "minute (median)", "holdout AUC after it (median)", "(mean)", "mentions depth/leaves", "mentions learning rate",
     "mentions trees/rounds", "mentions calendar", "runs with a kept depth/leaves change", "its minute (median)",
     "holdout AUC after the first kept depth/leaves change (median)"], rows)
out += "\nThe mention counts are regular-expression matches on the agent's own one-line description of the commit (heuristic).\n"
write("table_time_course.md", out, repo)

with open(RESULTS / "paths.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["run", "model", "minute", "holdout_auc", "eval_auc", "description"])
    for r in runs:
        for m_, h, e, d in r["path"]:
            w.writerow([r["run"], r["model"], f"{m_:.2f}", f"{h:.4f}", f"{e:.4f}", d])
with open(RESULTS / "first_keep_per_run.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["run", "model", "minute", "holdout_after", "eval_after", "description"])
    for r in runs:
        fk = C[r["run"]]["first_keep"]
        w.writerow([r["run"], r["model"]] + ([f"{fk[0]:.2f}", f"{fk[1]:.4f}", f"{fk[2]:.4f}", fk[3]] if fk else ["", "", "", ""]))
print("wrote results/paths.csv and results/first_keep_per_run.csv")
