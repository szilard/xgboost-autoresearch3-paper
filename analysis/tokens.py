#!/usr/bin/env python3
"""Token usage per run from the codex session logs, with a list-price projection (appendix)."""
import csv
import numpy as np
from common import MODELS, PRICES, RESULTS, SHORT, load_runs, md_table, runs_repo, write

repo = runs_repo()
runs = load_runs(repo)
rows = []
for r in runs:
    i, c, o = r["input_tokens"], r["cached_input_tokens"], r["output_tokens"]
    pi, pc, po = PRICES[r["model"]]
    r["cost_usd"] = ((i - c) * pi + c * pc + o * po) / 1e6
    r["cached_share"] = c / i
with open(RESULTS / "tokens_per_run.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["run", "model", "token_events", "input_tokens", "cached_input_tokens", "cached_share", "output_tokens",
                                   "reasoning_output_tokens", "total_tokens", "list_price_projection_usd", "holdout_auc", "experiments"])
    for r in runs:
        w.writerow([r["run"], r["model"], r["token_events"], r["input_tokens"], r["cached_input_tokens"], f"{r['cached_share']:.3f}",
                    r["output_tokens"], r["reasoning_output_tokens"], r["total_tokens"], f"{r['cost_usd']:.2f}", f"{r['holdout_auc']:.4f}", r["experiments"]])
for m in MODELS:
    rr = [r for r in runs if r["model"] == m]
    f = lambda k, s=1e6, d=1: (f"{np.mean([r[k] for r in rr])/s:.{d}f} ({min(r[k] for r in rr)/s:.{d}f} to {max(r[k] for r in rr)/s:.{d}f})")
    rows.append([SHORT[m], f("token_events", 1, 0), f("input_tokens"), f"{np.mean([r['cached_share'] for r in rr]):.1%}", f("output_tokens", 1e3, 0),
                 f("reasoning_output_tokens", 1e3, 0), f"{np.mean([r['cost_usd'] for r in rr]):.2f} ({min(r['cost_usd'] for r in rr):.2f} to {max(r['cost_usd'] for r in rr):.2f})",
                 f"{np.mean([r['cost_usd'] for r in rr]) / np.mean([r['input_tokens'] for r in rr]) * 1e6:.2f}"])
out = "## Token usage per run (mean, with min to max), from the session logs\n\n" + md_table(
    ["LLM", "token_count events", "input tokens, M", "cached share of input", "output tokens, K", "of which reasoning, K",
     "list-price projection per run, USD", "USD per M input tokens, effective"], rows)
out += ("\nTotals are the last cumulative `total_token_usage` of each session (checked to equal the sum of the per-event usage). "
        "The projection applies OpenAI's list prices per million tokens (input / cached input / output: "
        + "; ".join(f"{SHORT[m]} {PRICES[m][0]} / {PRICES[m][1]} / {PRICES[m][2]}" for m in MODELS)
        + ") to those totals. It is a projection, not a bill: the runs ran on a ChatGPT subscription. "
        "Reasoning tokens are a subset of output tokens.\n")
write("table_tokens.md", out, repo)
