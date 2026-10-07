#!/usr/bin/env python3
"""Collect the 60 runs into results/runs.csv, one row per run, cross-checked across sources."""
import csv
from common import RESULTS, header, load_runs, runs_repo, PAPER_ROOT

repo = runs_repo()
runs = load_runs(repo)
cols = ["group", "run", "model", "short", "effort", "codex_version", "driver_start", "driver_end",
        "clock_start_utc", "clock_stop_utc", "clock_elapsed_s", "clock_remaining_s", "experiments",
        "n_keep", "n_discard", "n_crash", "n_harness_runs", "best_commit", "best_eval_auc", "holdout_auc",
        "gap", "best_kept_holdout", "final_below_best", "ai_share_pct", "xgb_share_pct", "valid", "flags",
        "caveat_text", "integrity_flags", "protocol_flags", "turns_sent", "failed_turns", "retry_wait_s",
        "clock_stopped_by", "memory_peak_gib", "oom_kills", "compactions", "token_events", "input_tokens",
        "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens"]
RESULTS.mkdir(parents=True, exist_ok=True)
out = RESULTS / "runs.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["# " + header(repo).strip().replace("\n", " ")])
    w.writerow(cols)
    for r in runs:
        w.writerow([f"{r[c]:.4f}" if c in ("best_eval_auc", "holdout_auc", "gap", "best_kept_holdout") else r[c] for c in cols])
print(f"wrote {out.relative_to(PAPER_ROOT)}: {len(runs)} runs")
for m in ("gpt-6-astra", "gpt-6-sol", "gpt-6-luna"):
    rr = [r for r in runs if r["model"] == m]
    print(f"  {m}: {len(rr)} runs, {sum(r['valid']=='caveat' for r in rr)} with caveat, "
          f"{sum(r['integrity_flags']!='none' for r in rr)} with (cleared) integrity flags, "
          f"{sum(r['compactions']>0 for r in rr)} with context compaction, "
          f"dates {min(r['driver_start'] for r in rr)[:10]} to {max(r['driver_end'] for r in rr)[:10]}")
