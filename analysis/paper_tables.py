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
import re

repo = runs_repo()
runs = load_runs(repo)
OUT = PAPER_ROOT / "paper" / "tables"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1)


def save(name, headers, rows, caption):
    (OUT / f"{name}.md").write_text(md_table(headers, rows) + f"\nTable: {caption}\n")
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
     "Holdout AUC of each run's final model, 20 runs per LLM. The starter model scores 0.6725. sd is the sample standard deviation; the interval uses the t distribution; the percentiles are the nearest runs; the range is the best run minus the worst.")

# Table: head to head
rows = []
for a, b in itertools.combinations(MODELS, 2):
    A = [r["holdout_auc"] for r in model_runs(runs, a)]; B = [r["holdout_auc"] for r in model_runs(runs, b)]
    p, lo, hi = win(A, B)
    rows.append([f"{SHORT[a]} vs {SHORT[b]}", f"{p:.0%}", f"{lo:.0%}–{hi:.0%}", f"{np.mean(A)-np.mean(B):+.4f}"])
save("pairwise", ["pair", "P(first LLM's run wins)", "95% bootstrap interval", "difference of means"], rows,
     "Head to head: the probability that a randomly chosen run of the first LLM has a higher holdout AUC than a randomly chosen run of the second, over all 400 pairs of runs, ties counted half. Bootstrap: runs resampled within each LLM, 10,000 resamples.")

# Table: time course
C = {r["run"]: course(r) for r in runs}
rows = []
for m in MODELS:
    rr = model_runs(runs, m); cs = [C[r["run"]] for r in rr]
    med = lambda k: st.median([c[k] for c in cs if c[k] is not None])
    rows.append([SHORT[m], f"{med('first'):.1f}", f"{med('h15'):.4f}", f"{med('h30'):.4f}", f"{med('h45'):.4f}", f"{med('h60'):.4f}",
                 f"{st.mean(r['experiments'] for r in rr):.0f}", f"{st.mean(r['n_keep'] for r in rr):.1f}", f"{st.mean(r['ai_share_pct'] for r in rr):.0f}%",
                 f"{med('plateau'):.0f}", sum(c["plateau"] >= 20 for c in cs), f"{st.mean(c['downs'] for c in cs):.1f}"])
save("time_course", ["LLM", "first gain, min", "holdout at 15 min", "30 min", "45 min", "60 min", "experiments", "kept", "agent's share of the hour",
                     "longest plateau, min", "runs with a plateau of 20 min or more", "steps down per run"], rows,
     "The hour, per LLM. First gain: median minute of the first kept commit whose holdout AUC exceeds the starter's by more than 0.0005. Holdout at t: median over runs of the holdout AUC of the model kept at minute t. Experiments and kept commits: means per run. Agent's share: time outside XGBoost runs. Plateau: longest interval without a kept commit (median over runs). Steps down: kept commits whose holdout AUC is below the previous kept commit's (mean per run).")

# Table: first kept depth change
rows = []
for m in MODELS:
    fds = [C[r["run"]]["first_depth"] for r in model_runs(runs, m)]; fds = [x for x in fds if x]
    fks = [C[r["run"]]["first_keep"] for r in model_runs(runs, m)]; fks = [x for x in fks if x]
    rows.append([SHORT[m], f"{st.median(x[0] for x in fks):.1f}", f"{st.median(x[1] for x in fks):.4f}", len(fds), f"{st.median(x[0] for x in fds):.1f}", f"{st.median(x[1] for x in fds):.4f}"])
save("first_move", ["LLM", "first kept improvement, min", "holdout after it", "runs with a kept change to tree depth or leaves", "its minute", "holdout after it"], rows,
     "The first moves, medians over runs. A kept improvement is a kept commit with a higher eval AUC than the baseline's; a depth change is one whose description mentions depth, leaves or shallower trees.")

# Table: calendar audit
aud = {r["run"]: r for r in csv.DictReader(open(RESULTS / "feature_audit_per_run.csv"))}
rows = []
for m in MODELS:
    rr = model_runs(runs, m); a = [aud[r["run"]] for r in rr]
    kept = [r["holdout_auc"] for r, x in zip(rr, a) if x["dom_cat"] == "1"]; dropped = [r["holdout_auc"] for r, x in zip(rr, a) if x["dom_cat"] == "0"]
    rows.append([SHORT[m], len(dropped), sum(x["doy"] == "1" for x in a), sum(x["holiday"] == "1" for x in a), sum(x["month_cat"] == "0" for x in a),
                 f"{st.mean(dropped):.4f}" if dropped else "-", f"{st.mean(kept):.4f}" if kept else "-", f"{st.mean(dropped)-st.mean(kept):+.4f}" if kept and dropped else "-"])
save("calendar", ["LLM", "dropped the day-of-month category", "numeric day of year", "holiday features", "dropped the month category", "mean holdout, dropped", "mean holdout, kept", "difference"], rows,
     "How the 20 final models of each LLM handle the calendar, from an audit of their train.py. Means are holdout AUCs of the runs that dropped or kept the day-of-month category (Astra kept it in one run).")

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
     "Running the agent k times and keeping the run with the best eval AUC: median holdout AUC of the kept run, exact over the 20 observed runs with draws with replacement. The last two columns give, for k = 3, the 5th percentile of the kept run's holdout AUC and the median if the choice were made on the holdout set itself.")

# Appendix: tests
rows = []
for a, b in itertools.combinations(MODELS, 2):
    A = [r["holdout_auc"] for r in model_runs(runs, a)]; B = [r["holdout_auc"] for r in model_runs(runs, b)]
    t = ss.ttest_ind(A, B, equal_var=False); u = ss.mannwhitneyu(A, B, alternative="two-sided")
    gap = abs(np.mean(A) - np.mean(B)); sd = np.sqrt((np.var(A, ddof=1) + np.var(B, ddof=1)) / 2)
    rows.append([f"{SHORT[a]} vs {SHORT[b]}", f"{t.statistic:.1f}", f"{t.pvalue:.0e}", f"{u.statistic:.0f}", f"{u.pvalue:.0e}", f"{16*sd**2/gap**2:.0f}"])
f = ss.f_oneway(*[[r["holdout_auc"] for r in model_runs(runs, m)] for m in MODELS]); kw = ss.kruskal(*[[r["holdout_auc"] for r in model_runs(runs, m)] for m in MODELS])
save("tests", ["pair", "Welch t", "p", "Mann-Whitney U", "p", "runs per arm to detect the observed gap"], rows,
     f"Two-sided tests between LLMs and, post hoc, the runs per arm that the approximation 16 sd^2^ / gap^2^ gives for 80% power at the 5% level with the observed gap and pooled sd. One-way ANOVA: F = {f.statistic:.1f}, p = {f.pvalue:.0e}; Kruskal-Wallis: H = {kw.statistic:.1f}, p = {kw.pvalue:.0e}.")

# Appendix: sensitivity
subsets = [("all 60 runs", runs), ("without the 10 caveat runs", [r for r in runs if r["valid"] == "yes"]),
           ("without the 3 BTS-informed runs", [r for r in runs if r["run"] not in BTS_INFORMED])]
rows = []
for name, rs in subsets:
    means = [f"{np.mean([r['holdout_auc'] for r in model_runs(rs, m)]):.4f}" for m in MODELS]
    ps = [f"{win([r['holdout_auc'] for r in model_runs(rs, a)], [r['holdout_auc'] for r in model_runs(rs, b)])[0]:.0%}" for a, b in itertools.combinations(MODELS, 2)]
    rows.append([name, ", ".join(str(len(model_runs(rs, m))) for m in MODELS)] + means + ps)
save("sensitivity", ["runs", "n (Astra, Sol, Luna)", "mean Astra", "mean Sol", "mean Luna", "P(Astra beats Sol)", "P(Astra beats Luna)", "P(Sol beats Luna)"], rows,
     "The headline statistics without the runs with a protocol caveat and without the runs that used BTS documentation about the evaluation year (Astra 7 and 12, Sol 11).")

# Appendix: flags and caveats
rows = [[r["run"], r["integrity_flags"] if r["integrity_flags"] != "none" else "", r["flags"], note(r)]
        for r in runs if r["integrity_flags"] != "none" or r["valid"] == "caveat"]
save("flags", ["run", "integrity flag (cleared)", "caveat", "resolution"], rows,
     "The runs with an integrity flag from the automatic checks (all cleared on review) or a protocol caveat. No run was excluded.")

# Appendix: operations
rows = []
for m in MODELS:
    rr = model_runs(runs, m)
    rows.append([SHORT[m], f"{min(r['driver_start'][:10] for r in rr)} to {max(r['driver_end'][:10] for r in rr)}", sum(r["failed_turns"] for r in rr), sum(r["retry_wait_s"] > 0 for r in rr),
                 sum(r["clock_remaining_s"] < 0 for r in rr), f"{min(r['clock_elapsed_s'] for r in rr)//60}–{max(r['clock_elapsed_s'] for r in rr)//60} min",
                 sum(r["compactions"] > 0 for r in rr), f"{min(r['memory_peak_gib'] for r in rr)}–{max(r['memory_peak_gib'] for r in rr)}"])
save("operations", ["LLM", "dates (UTC)", "failed turns", "runs with retry waits", "runs stopped after the budget", "clock, min to max", "runs with a context compaction", "peak memory, GiB"], rows,
     "Operational summary. Failed turns ended with a service error (all but one with 'model at capacity') and were retried; the clock kept running. Every run's agent stopped the clock itself; the clock could exceed the hour when the agent's wrap-up came after its last status check. Nothing was killed at the 24 GB memory cap.")

# Appendix: tokens
rows = []
for m in MODELS:
    rr = model_runs(runs, m)
    cost = [((r["input_tokens"] - r["cached_input_tokens"]) * PRICES[m][0] + r["cached_input_tokens"] * PRICES[m][1] + r["output_tokens"] * PRICES[m][2]) / 1e6 for r in rr]
    rows.append([SHORT[m], f"{np.mean([r['input_tokens'] for r in rr])/1e6:.1f} ({min(r['input_tokens'] for r in rr)/1e6:.1f}–{max(r['input_tokens'] for r in rr)/1e6:.1f})",
                 f"{np.mean([r['cached_input_tokens']/r['input_tokens'] for r in rr]):.1%}", f"{np.mean([r['output_tokens'] for r in rr])/1e3:.0f}",
                 f"{np.mean([r['reasoning_output_tokens'] for r in rr])/1e3:.0f}", f"{np.mean([r['token_events'] for r in rr]):.0f}",
                 f"{np.mean(cost):.2f} ({min(cost):.2f}–{max(cost):.2f})"])
save("tokens", ["LLM", "input tokens, millions (min–max)", "cached share", "output tokens, thousands", "of which reasoning", "API responses", "list-price projection, USD (min–max)"], rows,
     "Token usage per run, means over the 20 runs, from the cumulative usage records in the session logs. The projection applies OpenAI's list prices per million tokens (input / cached input / output: Astra 10 / 1 / 50, Sol 2 / 0.20 / 10, Luna 0.10 / 0.01 / 0.50) and is not a bill: the runs ran on a ChatGPT subscription.")

# Appendix: per run
rows = []
for m in MODELS:
    for r in model_runs(runs, m):
        rows.append([r["run"], r["experiments"], r["n_keep"], f"{r['best_eval_auc']:.4f}", f"{r['holdout_auc']:.4f}", f"{r['gap']:+.4f}",
                     f"{r['clock_elapsed_s']//60}m{r['clock_elapsed_s']%60:02d}s", f"{r['ai_share_pct']:.0f}%", r["flags"] or ""])
save("per_run", ["run", "experiments", "kept", "eval AUC", "holdout AUC", "gap", "clock", "agent's share", "caveat"], rows,
     "The 60 runs. Experiments: rows of results.tsv, the baseline included. Kept: commits kept under the keep rule. Eval and holdout AUC: of the final model. Clock: from start to stop. Agent's share: time outside XGBoost runs.")

# Appendix: the example run's kept commits
ex = next(r for r in runs if r["run"] == "astra6_n20-1")
rows = [[f"{m_:.0f}", d, f"{e:.4f}", f"{h:.4f}"] for m_, h, e, d in ex["path"]]
save("example_run", ["minute", "the agent's description of the kept commit", "eval AUC", "holdout AUC"], rows,
     f"The {len(ex['path'])} kept commits of run {ex['run']}, in order, with the minute of the clock at which each was kept.")

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
        depth = a["max_depth"] or (f"{a['max_leaves']} leaves" if a["max_leaves"] else "")
        rows.append([r["run"], f"{r['holdout_auc']:.4f}", yn("dom_cat"), yn("month_cat"), yn("doy"), yn("holiday"), depth, a["n_estimators"], a["learning_rate"],
                     yn("ensemble"), a["verified"] or "pending"])
save("audit_per_run", ["run", "holdout AUC", "day-of-month category", "month category", "day of year", "holiday features", "depth", "trees", "learning rate", "ensemble", "checked by hand"], rows,
     "The final model of every run, from the scripted audit of its train.py. Depth: max_depth, or the leaf limit for lossguide trees; trees and learning rate as set in the file (the last assignment); ensemble: more than one model, seed averaging or a blend.")
