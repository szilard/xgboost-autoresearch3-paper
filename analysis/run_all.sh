#!/bin/bash
# Regenerate every table and figure of the paper from the runs repo.
# Usage: analysis/run_all.sh [path to xgboost-autoresearch-minimal3-runs]
set -euo pipefail
cd "$(dirname "$0")"
for s in collect_runs stats time_course feature_audit best_of_k gap tokens appendix_tables make_figures; do
  echo "== $s"; python3 $s.py "$@"
done
