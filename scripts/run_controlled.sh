#!/usr/bin/env bash
set -euo pipefail

COMMIT="ff7fc804f5c02e9b0a279790294350869663b4e2"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$ROOT/vendor"

mkdir -p "$WORK"
if [ ! -d "$WORK/KubeSec/.git" ]; then
  git clone https://github.com/paser-group/KubeSec.git "$WORK/KubeSec"
fi

cd "$WORK/KubeSec"
git fetch --all --tags
git checkout "$COMMIT"

python "$ROOT/patches/apply_repro_patch.py" "$WORK/KubeSec"
docker build -f Dockerfile.repro -t slikube-repro:"${COMMIT:0:8}" .

CONTROLLED="$ROOT/experiments/controlled"
docker run --rm   -v "$CONTROLLED:/iac"   slikube-repro:"${COMMIT:0:8}" /iac

python "$ROOT/scripts/analyze_results.py"   "$CONTROLLED/slikube_results.csv"   --expectations "$ROOT/experiments/controlled_expectations.csv"   --out "$ROOT/results/controlled_summary.csv"

echo
echo "Controlled reproduction complete."
echo "CSV:   $CONTROLLED/slikube_results.csv"
echo "SARIF: $CONTROLLED/SLIKUBE.sarif"
echo "Check: $ROOT/results/controlled_summary.csv"
