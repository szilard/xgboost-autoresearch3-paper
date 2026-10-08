#!/usr/bin/env python3
"""Appendix tables: the 60 runs, and the validity flags and caveats."""
import re
from common import MODELS, SHORT, load_runs, md_table, runs_repo, write

INTEGRITY_NOTES = {  # from the groups' results_summary.md and the runs' run.md
    "train_py_review": "false match: the check's pattern `glob` matches the word `global` in the variable name",
    "artifact_outside_clock": "explained: the artifact is from a harness run inside the clock that left no timing row of its own",
    "leak_check_hit": "false match: the leak check's content search matched a line that the agent had written itself",
}
GLOB_VARIABLE = {"sol6_n20-12": "global_delay_rate", "luna6_n20-1": "global_target_rate", "luna6_n20-7": "global_mean",
                 "luna6_n20-11": "global_delay_rate", "luna6_n20-15": "global_delay_rate"}  # from each run's checks.txt
SPECIAL = {"astra6_n20-15": "explained: a read of `data/train.csv` written differently from the starter, in a discarded commit",
           "astra6_n20-4": "explained: the last experiment, started inside the clock with 1m53s left (against the rule to stop with less than two minutes left, which no check enforces), was cut off during evaluation when the turn failed",
           "astra6_n20-16": "explained: the agent reset the repository before the evaluation of a discarded commit had finished, so its timing row carries the wrong commit",
           "astra6_n20-6": "false match: the leak check matched the end of a column list that the agent printed in its own setup check",
           "astra6_n20-8": "false match: the leak check matched a call to the harness's own artifact loader in the agent's final check"}


# caveat notes written in the same form for every run (the group summaries word them differently)
CAVEAT_NOTES = {
    "astra6_n20-5": '`7b7712f` (gamma 5) kept at a tie as "faster" by 0.8 s, within noise, not simpler; it stayed in the final model',
    "astra6_n20-8": '`e5e4a2b` (`max_cat_threshold` 16) kept at a tie as "faster" by 0.2 s, within noise, not simpler; it stayed in the final model',
    "astra6_n20-12": '`d4bd0fc` (`max_bin` 64) kept at a tie as "faster" by 1.1 s in one timing, within noise, not simpler; it stayed in the final model',
    "sol6_n20-8": '`83775c5` (DART `rate_drop` 0.2) kept at a tie as "faster" by 1.0 s, within noise, not simpler; it is the final model',
    "sol6_n20-19": '`f833740` (lossguide tree growth) kept at a tie as "faster" by 1.0 s, within noise, not simpler; lossguide stayed in the final model',
    "luna6_n20-6": '`bd192f4` (gamma 0.1) kept at a tie as "faster" by 0.6 s, within noise, not simpler; it changed neither the eval nor the holdout AUC',
    "luna6_n20-8": '`744ceef` and `7a1cbf0` (`min_child_weight` 5 and 10) kept at ties as "faster", within noise, not simpler; neither changed the eval or the holdout AUC',
    "luna6_n20-15": '`744705b` and `41db4a7` (gamma 1 and 2) kept at ties as "faster", within noise, not simpler; neither changed the eval or the holdout AUC, and gamma 2 stayed in the final model',
    "luna6_n20-18": '`dfccd9c` (gamma 1) kept at a tie as "faster" by 0.3 s, within noise, not simpler; it changed neither the eval nor the holdout AUC (the run also needed a second "go")',
    "sol6_n20-16": "7 failed turns, all 'model at capacity'; retry waits of 216 s",
}


def caveat_note(r):
    """The review's caveat text without the flag name (the table has its own column), in the paper's terms."""
    if r["run"] in CAVEAT_NOTES:
        return CAVEAT_NOTES[r["run"]]
    t = re.sub(r"^caveat:\s*(`?(keep_rule|turn_retries)`?:?\s*)?", "", r["caveat_text"])
    t = t.replace("Eval and Holdout AUC", "eval and holdout AUC").replace("best model", "final model")
    return t[:1].lower() + t[1:] if t[:1] != "`" else t


def note(r):
    parts = []
    if r["integrity_flags"] != "none":
        note = SPECIAL.get(r["run"]) or "; ".join(INTEGRITY_NOTES.get(f, f) for f in r["integrity_flags"].split())
        if r["run"] in GLOB_VARIABLE:
            note += f" `{GLOB_VARIABLE[r['run']]}`"
        parts.append(note)
    if r["caveat_text"]:
        parts.append(caveat_note(r))
    return "; ".join(parts)

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
