#!/usr/bin/env python3
"""Paper-ready tables (pandoc pipe tables with captions) in paper/tables/, from the same loaders as results/.

The paper's Markdown includes them with {{table:name}} markers that paper/build.py expands, so no
number in the paper is typed by hand.
"""
import itertools
import statistics as st
import numpy as np
from scipy import stats as ss
from common import BASE_EVAL, BASE_HOLDOUT, BTS_INFORMED, MODELS, PAPER_ROOT, PRICES, RESULTS, SHORT, load_runs, md_table, runs_repo
from best_of_k import dist, quantile
from time_course import course
from appendix_tables import note
import csv
import math
import re
from decimal import Decimal, ROUND_HALF_UP

repo = runs_repo()
runs = load_runs(repo)
OUT = PAPER_ROOT / "paper" / "tables"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1)


def rnd(x, nd=0):
    """Round half up (Python's own formatting rounds exact halves to even: 0.925 -> 92%, 2.25 -> 2.2)."""
    return Decimal(f"{float(x):.{nd + 6}f}").quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)


def pct(x, nd=0):
    return f"{rnd(100 * x, nd)}%"


def f1(x):
    return str(rnd(x, 1))


def xgb_seconds(r):
    """Mean duration of one experiment (training plus evaluation) in a run, from the harness timing rows."""
    v = []
    for x in csv.DictReader(open(r["dir"] / "timing" / "runs.tsv"), delimiter="\t"):
        try:
            v.append(float(x["train_s"]) + float(x["eval_s"]))
        except (ValueError, KeyError, TypeError):
            pass
    return st.mean(v)


def save(name, headers, rows, caption, **widths):
    (OUT / f"{name}.md").write_text(md_table(headers, rows, **widths) + f"\nTable: {caption}\n")
    print(f"wrote paper/tables/{name}.md")


def model_runs(rs, m):
    return [r for r in rs if r["model"] == m]


def win(A, B):
    A, B = np.array(A), np.array(B)
    w = (A[:, None] > B[None, :]) + 0.5 * (A[:, None] == B[None, :])
    ia = rng.integers(0, len(A), (10000, len(A))); ib = rng.integers(0, len(B), (10000, len(B)))
    boot = w[ia[:, :, None], ib[:, None, :]].mean(axis=(1, 2))
    return w.mean(), np.percentile(boot, 2.5), np.percentile(boot, 97.5)


# Table: per-LLM statistics
rows = []
for m in MODELS:
    x = np.array([r["holdout_auc"] for r in model_runs(runs, m)]); n = len(x)
    half = ss.t.ppf(0.975, n - 1) * x.std(ddof=1) / np.sqrt(n)
    p10, p90 = np.percentile(x, [10, 90], method="nearest")
    rows.append([SHORT[m], n, f"{x.mean():.4f}", f"{x.std(ddof=1):.4f}", f"{x.mean()-half:.4f}–{x.mean()+half:.4f}", f"{x.min():.4f}", f"{p10:.4f}",
                 f"{np.median(x):.4f}", f"{p90:.4f}", f"{x.max():.4f}", f"{x.mean()-BASE_HOLDOUT:+.4f}", f"{x.max()-x.min():.4f}"])
save("per_model", ["LLM", "n", "mean", "sd", "95% CI of the mean", "min", "10th pct.", "median", "90th pct.", "max", "mean gain over starter", "range"], rows,
     "Holdout AUC of each run's final model, 20 runs per LLM. The starter model scores 0.6725. sd is the sample standard deviation; the interval uses the t distribution; the 10th and 90th percentiles are the 3rd-lowest and 3rd-highest of the 20 runs; the range is the best run minus the worst.")

# Table: head to head
rows = []
for a, b in itertools.combinations(MODELS, 2):
    A = [r["holdout_auc"] for r in model_runs(runs, a)]; B = [r["holdout_auc"] for r in model_runs(runs, b)]
    p, lo, hi = win(A, B)
    rows.append([f"{SHORT[a]} vs {SHORT[b]}", pct(p), f"{pct(lo)}–{pct(hi)}", f"{np.mean(A)-np.mean(B):+.4f}"])
save("pairwise", ["pair", "P(first LLM's run wins)", "95% bootstrap interval", "difference of means"], rows,
     "Head to head: the probability that a randomly chosen run of the first LLM has a higher holdout AUC than a randomly chosen run of the second, over all 400 pairs of runs, ties counted half. Bootstrap: runs resampled within each LLM, 10,000 resamples.")

# Table: time course
C = {r["run"]: course(r) for r in runs}
rows = []
for m in MODELS:
    rr = model_runs(runs, m); cs = [C[r["run"]] for r in rr]
    med = lambda k: st.median([c[k] for c in cs if c[k] is not None])
    rows.append([SHORT[m], f"{med('h15'):.4f}", f"{med('h30'):.4f}", f"{med('h45'):.4f}", f"{med('h60'):.4f}",
                 f"{st.mean(r['experiments'] for r in rr):.0f}", f1(st.mean(r['n_keep'] for r in rr)), str(rnd(st.mean(xgb_seconds(r) for r in rr))),
                 f"{rnd(st.mean(r['ai_share_pct'] for r in rr))}%", f1(med('plateau')), sum(c["plateau"] >= 20 for c in cs), f1(st.mean(c['downs'] for c in cs))])
save("time_course", ["LLM", "holdout at 15 min", "30 min", "45 min", "60 min", "experiments", "kept", "experiment duration, s", "agent's share of the hour",
                     "longest plateau, min", "runs with a plateau of 20 min or more", "steps down per run"], rows,
     "The hour, per LLM. Holdout at t: median over runs of the holdout AUC of the model kept at minute t. Experiments and kept commits: means per run, the baseline counted as a kept commit. Experiment duration: mean time of one experiment, training and evaluation, in seconds. Agent's share: time outside experiments. Plateau: longest interval without a kept commit (median over runs). Steps down: kept commits whose holdout AUC is below the previous kept commit's (mean per run).")

# Table: first kept depth change
rows = []
for m in MODELS:
    fds = [C[r["run"]]["first_depth"] for r in model_runs(runs, m)]; fds = [x for x in fds if x]
    fks = [C[r["run"]]["first_keep"] for r in model_runs(runs, m)]; fks = [x for x in fks if x]
    rows.append([SHORT[m], f1(st.median(x[0] for x in fks)), f"{st.median(x[1] for x in fks):.4f}", len(fds), f1(st.median(x[0] for x in fds)), f"{st.median(x[1] for x in fds):.4f}"])
save("first_move", ["LLM", "first kept improvement, min", "holdout after it", "runs with a kept change to tree depth or leaves", "its minute", "holdout after it"], rows,
     "The first moves: medians over runs, except the count of runs with a depth change. A kept improvement is a kept commit with a higher eval AUC than the baseline's; a depth change is one whose description mentions depth, leaves or shallower trees.")

# Table: calendar audit
aud = {r["run"]: r for r in csv.DictReader(open(RESULTS / "feature_audit_per_run.csv"))}
rows = []
for m in MODELS:
    rr = model_runs(runs, m); a = [aud[r["run"]] for r in rr]
    kept = [r["holdout_auc"] for r, x in zip(rr, a) if x["dom_cat"] == "1"]; dropped = [r["holdout_auc"] for r, x in zip(rr, a) if x["dom_cat"] == "0"]
    rows.append([SHORT[m], len(dropped), sum(x["doy"] == "1" for x in a), sum(x["holiday"] == "1" for x in a), sum(x["month_cat"] == "0" for x in a),
                 f"{st.mean(dropped):.4f}" if dropped else "-", f"{st.mean(kept):.4f}" if kept else "-", f"{float(f'{st.mean(dropped):.4f}') - float(f'{st.mean(kept):.4f}'):+.4f}" if kept and dropped else "-"])
save("calendar", ["LLM", "dropped the day-of-month category", "numeric day-of-year-like feature", "holiday features", "dropped the month category", "mean holdout, dropped", "mean holdout, kept", "difference"], rows,
     "How the 20 final models of each LLM handle the calendar, from an audit of their train.py. Day-of-year-like: day, week or fortnight of the year as a number. Means are holdout AUCs of the runs that dropped or kept the day-of-month category (Astra kept it in one run); the difference is that of the means shown.")

# Table: eval-holdout gap
rows = []
for m in MODELS:
    rr = model_runs(runs, m); g = np.array([r["gap"] for r in rr]); e = [r["best_eval_auc"] for r in rr]; h = [r["holdout_auc"] for r in rr]
    rows.append([SHORT[m], f"{np.mean(e):.4f}", f"{np.mean(h):.4f}", f"{g.mean():+.4f}", f"{g.std(ddof=1):.4f}", f"{g.min():+.4f}", f"{g.max():+.4f}", f"{ss.spearmanr(e, h).correlation:.2f}"])
save("gap", ["LLM", "mean eval AUC", "mean holdout AUC", "mean gap", "sd", "min", "max", "rank correlation of eval and holdout AUC"], rows,
     f"Eval and holdout AUC of the final models and their gap (holdout minus eval). The starter's gap is {BASE_HOLDOUT-BASE_EVAL:+.4f}.")

# Table: best of k
KS = (1, 2, 3, 5, 10); rows = []
for m in MODELS:
    rr = model_runs(runs, m); e = np.array([r["best_eval_auc"] for r in rr]); h = np.array([r["holdout_auc"] for r in rr])
    rows.append([SHORT[m]] + [f"{quantile(dist(e, h, k), 0.5):.4f}" for k in KS] + [f"{quantile(dist(e, h, 3), 0.05):.4f}", f"{quantile(dist(h, h, 3), 0.5):.4f}"])
save("best_of_k", ["LLM"] + [f"k = {k}" for k in KS] + ["k = 3, 5th percentile", "k = 3, chosen on holdout"], rows,
     "Running the agent k times and choosing the run with the best eval AUC: median holdout AUC of the chosen run, computed exactly over the 20 observed runs with draws with replacement (for k = 1, the median of Table 2). The last two columns give, for k = 3, the 5th percentile of the chosen run's holdout AUC, from the same exact distribution, and the median if the choice were made on the holdout set itself.")

# Appendix: tests
rows = []
for a, b in itertools.combinations(MODELS, 2):
    A = [r["holdout_auc"] for r in model_runs(runs, a)]; B = [r["holdout_auc"] for r in model_runs(runs, b)]
    t = ss.ttest_ind(A, B, equal_var=False); u = ss.mannwhitneyu(A, B, alternative="two-sided")
    gap = abs(np.mean(A) - np.mean(B)); sd = np.sqrt((np.var(A, ddof=1) + np.var(B, ddof=1)) / 2)
    rows.append([f"{SHORT[a]} vs {SHORT[b]}", f"{t.statistic:.1f}", f"{t.pvalue:.0e}", f"{u.statistic:.0f}", f"{u.pvalue:.0e}", str(math.ceil(16 * sd**2 / gap**2))])
f = ss.f_oneway(*[[r["holdout_auc"] for r in model_runs(runs, m)] for m in MODELS]); kw = ss.kruskal(*[[r["holdout_auc"] for r in model_runs(runs, m)] for m in MODELS])
save("tests", ["pair", "Welch t", "p", "Mann-Whitney U", "p", "runs per arm to detect the observed gap"], rows,
     f"Two-sided tests between LLMs and, post hoc, the runs per arm, rounded up, that the approximation 16 sd^2^ / gap^2^ gives for 80% power at the 5% level with the observed gap and pooled sd. One-way ANOVA: F = {f.statistic:.1f}, p = {f.pvalue:.0e}; Kruskal-Wallis: H = {kw.statistic:.1f}, p = {kw.pvalue:.0e}.")

# Appendix: sensitivity
subsets = [("all 60 runs", runs), ("without the 10 caveat runs", [r for r in runs if r["valid"] == "yes"]),
           ("without the 3 BTS-informed runs", [r for r in runs if r["run"] not in BTS_INFORMED])]
rows = []
for name, rs in subsets:
    means = [f"{np.mean([r['holdout_auc'] for r in model_runs(rs, m)]):.4f}" for m in MODELS]
    ps = [pct(win([r['holdout_auc'] for r in model_runs(rs, a)], [r['holdout_auc'] for r in model_runs(rs, b)])[0]) for a, b in itertools.combinations(MODELS, 2)]
    rows.append([name, ", ".join(str(len(model_runs(rs, m))) for m in MODELS)] + means + ps)
save("sensitivity", ["runs", "n (Astra, Sol, Luna)", "mean Astra", "mean Sol", "mean Luna", "P(Astra beats Sol)", "P(Astra beats Luna)", "P(Sol beats Luna)"], rows,
     "The headline statistics without the runs with a protocol caveat and without the runs that used BTS documentation about the evaluation year (astra6_n20-7, astra6_n20-12 and sol6_n20-11).")

# Appendix: flags and caveats
rows = [[r["run"], r["integrity_flags"] if r["integrity_flags"] != "none" else "", r["flags"], note(r)]
        for r in runs if r["integrity_flags"] != "none" or r["valid"] == "caveat"]
save("flags", ["run", "integrity flag (cleared)", "caveat", "resolution"], rows,
     "The runs with an integrity flag, the leak check included (all false alarms on review), or a protocol caveat. No run was excluded.")

# Appendix: operations
rows = []
for m in MODELS:
    rr = model_runs(runs, m)
    rows.append([SHORT[m], f"{min(r['driver_start'][:10] for r in rr)} to {max(r['driver_end'][:10] for r in rr)}", sum(r["failed_turns"] for r in rr), sum(r["retry_wait_s"] > 0 for r in rr),
                 sum(r["clock_remaining_s"] < 0 for r in rr), "–".join(f"{t//60}:{t%60:02d}" for t in (min(r['clock_elapsed_s'] for r in rr), max(r['clock_elapsed_s'] for r in rr))),
                 sum(r["compactions"] > 0 for r in rr), f"{min(r['memory_peak_gib'] for r in rr)}–{max(r['memory_peak_gib'] for r in rr)}"])
save("operations", ["LLM", "dates (UTC)", "failed turns", "runs with retry waits", "runs stopped after the budget", "clock, min:s, shortest to longest", "runs with a context compaction", "peak memory, GiB"], rows,
     "Operational summary. Failed turns ended with the service error 'model at capacity' and were retried; the clock kept running. Every run's agent stopped the clock itself; the clock could exceed the hour when the agent's wrap-up came after its last status check. Nothing was killed at the 24 GiB memory cap.")

# Appendix: tokens
rows = []
for m in MODELS:
    rr = model_runs(runs, m)
    cost = [((r["input_tokens"] - r["cached_input_tokens"]) * PRICES[m][0] + r["cached_input_tokens"] * PRICES[m][1] + r["output_tokens"] * PRICES[m][2]) / 1e6 for r in rr]
    rows.append([SHORT[m], f"{np.mean([r['input_tokens'] for r in rr])/1e6:.1f} ({min(r['input_tokens'] for r in rr)/1e6:.1f}–{max(r['input_tokens'] for r in rr)/1e6:.1f})",
                 pct(np.mean([r['cached_input_tokens'] / r['input_tokens'] for r in rr]), 1), f"{np.mean([r['output_tokens'] for r in rr])/1e3:.0f}",
                 f"{np.mean([r['reasoning_output_tokens'] for r in rr])/1e3:.0f}", f"{np.mean([r['token_events'] for r in rr]):.0f}",
                 f"{np.mean(cost):.2f} ({min(cost):.2f}–{max(cost):.2f})"])
save("tokens", ["LLM", "input tokens, millions (min–max)", "cached share", "output tokens, thousands", "of which reasoning", "API responses", "list-price projection, USD (min–max)"], rows,
     "Token usage per run, means over the 20 runs, from the cumulative usage records in the session logs. The projection applies OpenAI's list prices per million tokens (input / cached input / output: Astra 10 / 1 / 50, Sol 2 / 0.20 / 10, Luna 0.10 / 0.01 / 0.50) and is not a bill: the runs ran on a ChatGPT subscription.")

# Appendix: per run
rows = []
for m in MODELS:
    for r in model_runs(runs, m):
        rows.append([r["run"], r["experiments"], r["n_keep"], f"{r['best_eval_auc']:.4f}", f"{r['holdout_auc']:.4f}", f"{r['gap']:+.4f}",
                     f"{r['clock_elapsed_s']//60}m{r['clock_elapsed_s']%60:02d}s", f"{rnd(r['ai_share_pct'])}%", r["flags"] or ""])
save("per_run", ["run", "experiments", "kept", "eval AUC", "holdout AUC", "gap", "clock", "agent's share", "caveat"], rows,
     "The 60 runs. Experiments: rows of results.tsv, the baseline included. Kept: kept commits, the baseline included. Eval and holdout AUC: of the final model. Clock: from start to stop. Agent's share: time outside experiments.")

# Appendix: the example run's kept commits
ex = next(r for r in runs if r["run"] == "astra6_n20-1")
rows = [[f"{m_:.0f}", d, f"{e:.4f}", f"{h:.4f}"] for m_, h, e, d in ex["path"]]
save("example_run", ["minute", "the agent's description of the kept commit", "eval AUC", "holdout AUC"], rows,
     f"The baseline and the {len(ex['path']) - 1} kept changes of run {ex['run']}, in order, with the minute of the clock at which each was kept.")

# Appendix: the rules given to the agent, from program.md of the minimal3 repo at the pinned commit
m3 = PAPER_ROOT.parent / "xgboost-autoresearch-minimal3" / "program.md"
if m3.exists():
    lines = m3.read_text().splitlines()
    def section(start, end_prefixes):
        i = next(i for i, l in enumerate(lines) if l.startswith(start))
        j = next((k for k in range(i + 1, len(lines)) if any(lines[k].startswith(p) for p in end_prefixes)), len(lines))
        return lines[i:j]
    parts = section("**The task:**", ["## Setup"]) + [""] + section("## Experimentation", ["## Research"]) + [""] + \
            section("**Keep rule**", ["**The first run**"]) + [""] + section("## The experiment loop", ["**Timeout**"]) + [""] + \
            section("**Time budget**", ["When `python3 harness.py status`"])
    parts = [re.sub(r"^#+\s*(.*)$", r"**\1**", l) for l in parts]
    fixed = []
    for l in parts:  # pandoc needs a blank line between a paragraph and a list
        if re.match(r"^\s*(-|\d+\.)\s", l) and fixed and fixed[-1].strip() and not re.match(r"^\s*(-|\d+\.)\s", fixed[-1]):
            fixed.append("")
        fixed.append(l)
    parts = fixed
    text = "\n".join("> " + l if l.strip() else ">" for l in parts)
    (OUT / "program_rules.md").write_text(text + "\n")
    print("wrote paper/tables/program_rules.md")
else:
    print("warning: minimal3 repo not found; program_rules.md not regenerated")

# Appendix: the feature audit per run
rows = []
for m in MODELS:
    for r in model_runs(runs, m):
        a = aud[r["run"]]
        yn = lambda k: "yes" if a[k] == "1" else ""
        if a["verified"]:  # settings as read in the manual audit; "16 leaves" kept on one line
            depth, trees, lrate = (re.sub(r"(\d) leaves", r"\1\\ leaves", a[k]) for k in ("depth_read", "trees_read", "learning_rate_read"))
        else:
            leaves = a["max_leaves_all"].split("/")[-1] if a["max_leaves_all"] else ""
            depth = ", ".join((f"{leaves}\\ leaves" if leaves else "lossguide") if d == "0" else d for d in a["max_depth_all"].split("/")) if a["max_depth_all"] else ""
            trees, lrate = (a[k].replace("/", ", ") for k in ("n_estimators_all", "learning_rate_all"))  # a comma and a space, so that the cell can wrap
        rows.append([r["run"], f"{r['holdout_auc']:.4f}", yn("dom_cat"), yn("month_cat"), yn("doy"), yn("holiday"), depth, trees, lrate,
                     yn("ensemble"), a["verified"] or "pending"])
verified_all = all(aud[r["run"]]["verified"] for r in runs)
save("audit_per_run", ["run", "holdout AUC", "day-of-month category", "month category", "day-of-year-like", "holiday features", "depth", "trees", "learning rate", "ensemble",
                       "verified" if verified_all else "checked by hand"], rows,
     ("The final model of every run. A script read each final train.py; every file was then read in full, and the script's verdicts were confirmed or corrected (Appendix E). "
      "Depth, trees and learning rate as read for the models of the final prediction, each distinct value once, in the order of the file; \"16 leaves\" is a leaf limit for lossguide trees. "
      "Ensemble: the prediction combines more than one fitted model (different configurations, seeds or a blend).")
     if verified_all else
     "The final model of every run, from the scripted audit of its train.py. Depth: max_depth, or the leaf limit for lossguide trees (lossguide alone where the script could not read the limit). Where a file sets a value more than once, as ensembles of different models do, every value is listed in the order of the file. A blank means the file computes the value rather than setting a number. Ensemble: more than one model, seed averaging or a blend.",
     max_wrapping=12)  # eleven columns: the settings columns wrap so that run names keep one line
