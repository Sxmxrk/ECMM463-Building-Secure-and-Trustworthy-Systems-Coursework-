# Reproducing and verifying the package

These commands are written for Windows PowerShell from the extracted package root. On Linux/macOS, the Python commands are identical; run the Docker command shown below instead of the PowerShell runner.

## 1. Check the supplied evidence (no Docker needed)

```powershell
python .\scripts\verify_submission.py
```

The check compares the 2,031 saved M08 scanner rows against the authors' 20 fields (**40,620 comparisons**); verifies the M08 manifest SHA-256 inventory; confirms that exactly 46 files were selected; checks the historical evidence blobs and template additions; and reconciles the M07/M08 counts. It does not invoke the scanner and should not be cited as a fresh scanner run.

## 2. Rebuild M08 from M07 and compact evidence

```powershell
python .\scripts\rebuild_m08.py --plan
python .\scripts\rebuild_m08.py --build
```

This creates `experiments/figshare_recovery_M08_rebuilt/` only when that directory does not exist. It recreates 40 changed manifest blobs plus seven chart contexts from the 46 documented selections and 51 added template files. SHA-256 checks ensure the rebuilt tree is byte-identical to the supplied M08. The frozen M07 and provided M08 are never overwritten.

## 3. Rescan the archived M08 input in Docker

Prerequisites: a running Docker Desktop / Docker Engine. The image uses Python 3.10 and dependency versions specified in `figshare_tool/Dockerfile`.

```powershell
# The script builds the original paper-era scanner image if needed.
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\run_m08.ps1
```

Outputs are created in `results/verification_run/`, separate from the supplied results. An existing complete output file is never overwritten. A full historical scan may be computationally expensive, especially for very large YAML manifests.

Linux/macOS equivalent:

```bash
docker build -t slikube-figshare-paper:2021 ./figshare_tool
mkdir -p results/verification_run
docker run --rm -v "$(pwd):/project:ro" -v "$(pwd)/results/verification_run:/results" \
  --entrypoint python slikube-figshare-paper:2021 \
  /project/scripts/scan_M08_docker.py --root /project --out /results
```

## 4. Verify newly scanned output

After the Docker run, inspect `results/verification_run/figshare_M08_summary.csv` and `results/verification_run/figshare_M08_full20_per_file.csv`. The target is 2,031 exact matches across all 20 fields. Differences must be recorded as new observations rather than changing the historical record or overriding benchmark files.

## 5. Optional controlled test suite

The controlled pairs are under `experiments/controlled/`. The 2023 KubeSec verification path uses a separate pinned source and documented patch. If Git and Docker are available, run `scripts/run_controlled.ps1`. Its results are already preserved in `results/controlled_summary.csv`; this run is separate from M07/M08.

## Guardrails

- No script in the normal workflow overwrites M07 or the supplied M08.
- `scripts/rebuild_m08.py` rejects an existing target folder.
- `scripts/run_m08.ps1` writes to a separate verification directory.
- `scripts/verify_submission.py` uses the Python standard library and performs no network operations.
- The full source recovery workflow required historical external repositories and is not necessary for reproducing the frozen comparison.
