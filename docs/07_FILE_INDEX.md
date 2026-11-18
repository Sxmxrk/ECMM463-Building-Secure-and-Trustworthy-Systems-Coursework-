# Package file index

| Location | Purpose |
|---|---|
| `README.md` | Entry point and interpretation |
| `docs/` | Methods, results, limitations, runbook, report brief and presentation plan |
| `figshare_tool/` | Paper-era detector modules, reproduction launcher and Docker build recipe |
| `figshare_source/` | Published URL, metric and repository-list CSVs |
| `experiments/controlled/` | Predeclared secure/insecure test manifests and recorded outputs |
| `experiments/figshare_reconstructed/` | Initial partial dataset reconstruction |
| `experiments/figshare_recovery_M02/` to `M06/` | Earlier historical recovery snapshots (archival) |
| `experiments/figshare_recovery_M07/` | Frozen recovered-source baseline; scanner CSV included |
| `experiments/figshare_recovery_M08/` | Frozen integrated historical-source sensitivity dataset |
| `results/` | Primary comparable expected values, M07 and M08 reports |
| `evidence/source_selection.csv` | Commit, date and hash provenance for exactly 46 selected cases |
| `evidence/candidate_files/` | Exactly 46 staged source files from the M08 selection |
| `evidence/template_additions/` | Exactly 51 chart templates needed to reconstruct the M08 context |
| `evidence/investigation_reports/` | Selected supporting case-by-case experimental reports |
| `archive/results/` | Earlier recovery and diagnostic outputs retained for audit history |
| `scripts/verify_submission.py` | Dependency-free verification of hashes, row sets and scanner values |
| `scripts/rebuild_m08.py` | Non-destructive reconstruction from M07 plus compact evidence |
| `scripts/scan_M08_docker.py` | 20-field runner for unchanged paper-era scanner |
| `scripts/run_m08.ps1` | Windows Docker orchestration with separate output directory |
| `patches/` | Documented adaptation for the separate 2023 controlled test path |
| `SHA256SUMS.txt` | Checksums for the delivered artefact's individual files |
| `docs/08_VERIFICATION_RECORD.md` | Release verification steps and environment scope |

**Scope of this distribution:** Git recovery caches and intermediate investigation scripts are excluded because the frozen datasets, hashes, source candidates and measured outputs are sufficient for the comparison and rebuild workflows. The original uploaded project archive remains unchanged.
