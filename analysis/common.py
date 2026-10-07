"""Shared loaders for the paper's analysis scripts.

Every script reads the archived runs of xgboost-autoresearch-minimal3-runs (run-multi/<group>/)
and writes its printed output under analysis/results/, with the command and the runs repo commit
on the first lines. Nothing here touches the runs repo.
"""
import csv
import gzip
import json
import re
import statistics as st
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER_ROOT = HERE.parent
RESULTS = HERE / "results"
FIGURES = PAPER_ROOT / "figures"
DEFAULT_RUNS_REPO = PAPER_ROOT.parent / "xgboost-autoresearch-minimal3-runs"

GROUPS = {"astra6_n20": "gpt-6-astra", "sol6_n20": "gpt-6-sol", "luna6_n20": "gpt-6-luna"}
MODELS = ["gpt-6-astra", "gpt-6-sol", "gpt-6-luna"]  # best mean on top, as in the blog's plots
SHORT = {"gpt-6-astra": "Astra", "gpt-6-sol": "Sol", "gpt-6-luna": "Luna"}
COLOUR = {"gpt-6-astra": "#2a78d6", "gpt-6-sol": "#eb6834", "gpt-6-luna": "#1baf7a"}
BASE_EVAL, BASE_HOLDOUT = 0.6743, 0.6725
# OpenAI list prices per million tokens (input, cached input, output), from the model pages
# developers.openai.com/api/docs/models/gpt-6-{astra,sol,luna}, read 2026-10-07. A projection
# only: the runs were made on a ChatGPT subscription and no metered spend occurred.
PRICES = {"gpt-6-astra": (10.0, 1.0, 50.0), "gpt-6-sol": (2.0, 0.2, 10.0), "gpt-6-luna": (0.1, 0.01, 0.5)}
# runs that used BTS/TranStats documentation about the eval year (see the group summaries)
BTS_INFORMED = {"astra6_n20-7", "astra6_n20-12", "sol6_n20-11"}


def runs_repo():
    p = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else DEFAULT_RUNS_REPO
    if not (p / "run-multi").is_dir():
        sys.exit(f"runs repo not found at {p} (pass its path as the first argument)")
    return p.resolve()


def repo_commit(p):
    try:
        return subprocess.check_output(["git", "-C", str(p), "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def header(repo):
    cmd = " ".join(["analysis/" + Path(sys.argv[0]).name] + sys.argv[1:])
    return (f"<!-- {cmd} -->\n<!-- runs repo: {repo} @ {repo_commit(repo)}; "
            f"generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')} -->\n\n")


def write(name, text, repo):
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / name
    out.write_text(header(repo) + text)
    print(f"wrote {out.relative_to(PAPER_ROOT)}")


def tsv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


def utc(ts):
    return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def md_table(headers, rows, min_width=4, max_wrapping=50):
    """Pipe table; the separator's dash counts set pandoc's relative column widths when a row is wider than
    the line length. A column needs room for its longest unbreakable piece (a header word, or a whole cell
    when the column's cells contain no spaces) plus the cell padding; the n // 3 covers digits and capitals,
    which are wider than the average letter."""
    def need(n):
        return n + 2 + n // 3
    cells = [[str(c) for c in r] for r in rows]
    widths = []
    for j, h in enumerate(headers):
        longest_word = max([len(w) for w in re.split(r"[\s-]+", str(h))] + [1])
        col = [r[j] for r in cells if j < len(r)]
        body = max([len(c) for c in col] + [1])
        no_space = all(" " not in c.replace("\\ ", "") for c in col)  # "\ " is pandoc's non-breaking space
        widths.append(max(min_width, need(longest_word), need(body) + (3 if body >= 8 else 0) if no_space else min(body, max_wrapping)))  # long unbreakable cells (run names, "confirmed") need a margin
    out = ["| " + " | ".join(str(h) for h in headers) + " |", "|" + "|".join("-" * w for w in widths) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in cells]
    return "\n".join(out) + "\n"


def f4(x):
    return "-" if x is None else f"{x:.4f}"


def session_stats(gz):
    """(compactions, tokens dict, token_count events) from a slimmed codex session log."""
    compactions, events, tokens = 0, 0, {}
    with gzip.open(gz, "rt") as f:
        for line in f:
            d = json.loads(line)
            if d.get("type") == "compacted":
                compactions += 1
            elif d.get("type") == "event_msg" and d.get("payload", {}).get("type") == "token_count":
                events += 1
                info = d["payload"].get("info") or {}
                if info.get("total_token_usage"):
                    tokens = info["total_token_usage"]  # cumulative over the session; keep the last
    return compactions, tokens, events


def keep_path(rd):
    """[(minutes since clock start, holdout AUC)] of the kept commits, and the clock's end in minutes.

    A kept commit counts from the end of its first completed harness run (as the runs repo's
    plotting tool does).
    """
    clock = json.loads((rd / "timing" / "clock.json").read_text())
    end = {}
    for r in tsv(rd / "timing" / "runs.tsv"):
        if r["status"] == "ok":
            end.setdefault(r["commit"], (float(r["end"]) - clock["start"]) / 60)
    path = []
    for r in tsv(rd / "holdout_scores.tsv"):
        if r["status"] == "keep" and r["holdout_auc"] not in ("", "N/A", "CRASH"):
            if r["commit"] not in end:
                sys.exit(f"{rd.name}: kept commit {r['commit']} has no completed harness run")
            path.append((end[r["commit"]], float(r["holdout_auc"]), float(r["eval_auc"]), r["description"]))
    return path, (clock["stop"] - clock["start"]) / 60, clock


def caveat_text(repo):
    """{run: text of the 'caveat / excluded' column of the group's results_summary.md}."""
    out = {}
    for g in GROUPS:
        for line in (repo / "run-multi" / g / "results_summary.md").read_text().splitlines():
            if line.startswith(f"| {g}-"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                out[cells[0]] = cells[-1]
    return out


def load_runs(repo, with_session=True):
    """One dict per run, all 60, in group order then run number."""
    cav = caveat_text(repo)
    runs = []
    for g, model in GROUPS.items():
        gdir = repo / "run-multi" / g
        for r in sorted(tsv(gdir / "holdout_auc.tsv"), key=lambda r: int(r["run"].rsplit("-", 1)[1])):
            rd = gdir / r["run"]
            ds = json.loads((rd / "driver-summary.json").read_text())
            assert ds["model"] == model and ds["best_holdout_auc"] == r["holdout_auc"], r["run"]
            rep = (rd / "report.txt").read_text()
            ai = float(re.search(r"^AI:\s+\S+\s+([\d.]+)%", rep, re.M).group(1))
            xg = float(re.search(r"^XGBoost runs:\s+\S+\s+([\d.]+)%", rep, re.M).group(1))
            n_h = int(re.search(r"\((\d+) runs:", rep).group(1))
            rows = tsv(rd / "results.tsv")
            status = [x["status"].strip() for x in rows]
            path, end_min, clock = keep_path(rd)
            best_kept = max(h for _, h, _, _ in path)
            drv = (rd / "driver.log").read_text(errors="replace").splitlines()
            leak = re.search(r"^CONTENT HITS: (\d+)", (rd / "leak_check.txt").read_text(errors="replace"), re.M)
            leak_hits = int(leak.group(1)) if leak else -1
            integrity = ds["integrity_flags"]  # run_checks.py; a content hit of the leak check is added as a flag of its own
            if leak_hits > 0:
                integrity = "leak_check_hit" if integrity == "none" else integrity + " leak_check_hit"
            d = dict(
                group=g, run=r["run"], model=model, short=SHORT[model], effort=ds["effort"],
                codex_version=ds["codex_version"], driver_start=drv[0][:20], driver_end=drv[-1][:20],
                clock_start_utc=utc(clock["start"]), clock_stop_utc=utc(clock["stop"]),
                clock_elapsed_s=ds["clock_elapsed_s"], clock_remaining_s=ds["clock_remaining_s"],
                experiments=int(r["experiments"]), n_keep=status.count("keep"), n_discard=status.count("discard"),
                n_crash=status.count("crash"), n_harness_runs=n_h, best_commit=r["best_commit"],
                best_eval_auc=float(r["eval_auc"]), holdout_auc=float(r["holdout_auc"]), gap=float(r["gap"]),
                best_kept_holdout=best_kept, final_below_best=int(float(r["holdout_auc"]) < best_kept - 1e-9),
                ai_share_pct=ai, xgb_share_pct=xg, valid=r["valid"], flags=r["flags"], caveat_text=cav.get(r["run"], ""),
                integrity_flags=integrity, protocol_flags=ds["protocol_flags"], leak_content_hits=leak_hits,
                turns_sent=len(ds["turns"]), failed_turns=ds["failed_turns"], retry_wait_s=ds["retry_wait_s"],
                clock_stopped_by=ds["clock_stopped_by"], memory_peak_gib=round(int(ds["memory_peak_bytes"]) / 2**30, 1),
                oom_kills=int(ds["oom_kills"]), path=path, end_min=end_min, dir=rd,
            )
            assert d["experiments"] == len(rows) == ds["results_rows"], r["run"]
            if with_session:
                comp, tok, ev = session_stats(rd / "codex-session.jsonl.gz")
                d.update(compactions=comp, token_events=ev, input_tokens=tok.get("input_tokens"),
                         cached_input_tokens=tok.get("cached_input_tokens"), output_tokens=tok.get("output_tokens"),
                         reasoning_output_tokens=tok.get("reasoning_output_tokens"), total_tokens=tok.get("total_tokens"))
            runs.append(d)
    assert len(runs) == 60 and all(r["valid"] in ("yes", "caveat") for r in runs)
    return runs


def by_model(runs, key="holdout_auc"):
    return {m: [r[key] for r in runs if r["model"] == m] for m in MODELS}


def runs_csv(repo):
    """The collected table written by collect_runs.py, re-read as dicts (numbers as strings)."""
    with open(RESULTS / "runs.csv", newline="") as f:
        return list(csv.DictReader(f))
