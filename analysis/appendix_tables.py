#!/usr/bin/env python3
"""Appendix tables: the 60 runs, and the validity flags and caveats."""
from common import MODELS, SHORT, load_runs, md_table, runs_repo, write

INTEGRITY_NOTES = {  # from the groups' results_summary.md and the runs' run.md
    "train_py_review": "false match: the check's pattern `glob` matches the word `global` in a variable name (e.g. `global_target_rate`)",
    "artifact_outside_clock": "explained: the artifact is from a harness run inside the clock that left no timing row of its own",
}
SPECIAL = {"astra6_n20-15": "explained: a read of `data/train.csv` written differently from the starter, in a discarded commit",
           "astra6_n20-4": "explained: the last experiment, started inside the clock with 1m53s left, was cut off during evaluation when the turn failed",
           "astra6_n20-16": "explained: a discarded run whose timing row got the wrong commit after a bookkeeping slip by the agent"}
def note(r):
    if r["caveat_text"]:
        return r["caveat_text"]
    if r["run"] in SPECIAL:
        return SPECIAL[r["run"]]
    return "; ".join(INTEGRITY_NOTES.get(f, f) for f in r["integrity_flags"].split())


def main():
    repo = runs_repo()
    runs = load_runs(repo)
    rows = []
    for m in MODELS:
        for r in [r for r in runs if r["model"] == m]:
            rows.append([r["run"], r["experiments"], r["n_keep"], f"{r['best_eval_auc']:.4f} (`{r['best_commit']}`)", f"{r['holdout_auc']:.4f}",
                         f"{r['gap']:+.4f}", f"{r['clock_elapsed_s']//60}m{r['clock_elapsed_s']%60:02d}s", f"{r['ai_share_pct']:.0f}%",
                         r["valid"], r["flags"] or ""])
    write("appendix_per_run.md", "## The 60 runs\n\n" + md_table(
        ["run", "experiments", "kept", "best eval AUC (commit)", "holdout AUC", "gap", "clock", "AI share", "valid", "caveat"], rows)
        + "\nexperiments: rows of results.tsv, the baseline included; kept: commits kept under the keep rule; clock: time from `harness.py start` "
        "to `harness.py stop`; AI share: time outside harness runs.\n", repo)

    flag_rows = [[r["run"], r["integrity_flags"], r["protocol_flags"], r["valid"], r["flags"], note(r)]
                 for r in runs if r["integrity_flags"] != "none" or r["valid"] == "caveat" or r["protocol_flags"] != "none"]
    ops = []
    for m in MODELS:
        rr = [r for r in runs if r["model"] == m]
        ops.append([SHORT[m], sum(r["turns_sent"] for r in rr) - 2 * len(rr), sum(r["failed_turns"] for r in rr), sum(r["retry_wait_s"] > 0 for r in rr),
                    sum(r["clock_stopped_by"] != "agent" for r in rr), sum(r["clock_remaining_s"] < 0 for r in rr), sum(r["compactions"] > 0 for r in rr),
                    f"{min(r['memory_peak_gib'] for r in rr)} to {max(r['memory_peak_gib'] for r in rr)}", sum(r["oom_kills"] for r in rr)])
    write("appendix_flags.md", "## Runs with integrity flags (all cleared on review) or protocol caveats\n\n" + md_table(
        ["run", "integrity flags (run_checks.py)", "protocol flags (run_checks.py)", "valid", "caveat flags (review)", "review note"], flag_rows)
        + "\n## Operational summary per LLM\n\n" + md_table(
        ["LLM", "turns sent beyond the prompt and one go (retries included)", "failed turns", "runs with retry waits", "runs where the driver stopped the clock",
         "runs that stopped after the budget", "runs with a context compaction", "peak memory, GiB", "processes killed at the cap"], ops), repo)


if __name__ == "__main__":
    main()
