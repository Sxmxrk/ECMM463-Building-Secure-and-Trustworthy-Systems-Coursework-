# SLI-KUBE — Reproduction and Historical Source Sensitivity Study

**Research reproduction package | 10 November 2026**

This archive reproduces and investigates the security-misconfiguration results reported by Rahman et al. in *Security Misconfigurations in Open Source Kubernetes Manifests: An Empirical Study*. It contains the original released scanner code, paper result data, a recovered manifest corpus, controlled tests, frozen experimental snapshots, source provenance and verification scripts.

## Primary results

| Measure | M07 — recovered baseline | M08 — historical-source sensitivity |
|---|---:|---:|
| Manifests evaluated | 2,031 | 2,031 |
| Exact matches, 13 headline fields | 1,991 (98.03%) | 2,031 (100.00%) |
| Exact matches, all 20 output fields | 1,985 (97.74%) | 2,031 (100.00%) |
| Alternatives to M07 source/context | — | 46 |

**Interpretation:** M07 is the principal historical-source reproduction. M08 is a second, explicitly outcome-informed sensitivity experiment: 39 alternative manifest versions and seven Helm chart contexts were chosen after evaluating differences from published results. The M08 100% match is *conditional agreement for the 2,031 comparable files*, not proof that the original manifest snapshots used by the authors were uniquely recovered or that the scanner would agree on independent, previously unseen data.

The original archive lists **2,039 manifest paths**. Eight are outside the M07/M08 comparable scan set. One original `sa-traefik` manifest is not recovered; one historical source has an independently verified empty Git blob. The remaining excluded entries are documented in the recovery reports. Two of the 39 substituted manifest versions have commits after the historical cutoff; excluding these two cases yields **2,029 / 2,031 (99.90%)** as the stricter sensitivity calculation.

## Getting started (Windows PowerShell)

From the extracted archive's root:

```powershell
python .\scripts\verify_submission.py

# Rebuild M08 independently from M07 and the evidence files.
python .\scripts\rebuild_m08.py --build

# Run the paper-era scanner again; outputs go to a new directory.
.\scripts\run_m08.ps1
```

`verify_submission.py` needs only Python 3.10+ standard-library modules. Rebuilding creates a new directory and never overwrites the supplied M08 or M07. Rescanning uses Docker Desktop / Docker Engine and a paper-era scanner image built from `figshare_tool/Dockerfile`.

**Full instructions:** [docs/04_REPRODUCING_THE_RESULTS.md](docs/04_REPRODUCING_THE_RESULTS.md).

## Documentation

- [Study design and implementation](docs/01_METHODS.md)
- [Measured results and reconciliation](docs/02_RESULTS.md)
- [Scope and provenance limitations](docs/03_LIMITATIONS.md)
- [Reproduction procedures](docs/04_REPRODUCING_THE_RESULTS.md)
- [Technical report handoff](docs/05_REPORT_BRIEF.md)
- [Ten-minute presentation plan](docs/06_PRESENTATION_PLAN.md)
- [Package directory guide](docs/07_FILE_INDEX.md)

## Data handling and attribution

This repository contains archived research examples, including manifest values flagged by the secret scanner. Treat these as historical samples, **not deployment templates**. No credentials are needed to read or verify the package. Do not execute any manifest against a live cluster.

**Paper:** Rahman et al., *Security Misconfigurations in Open Source Kubernetes Manifests: An Empirical Study*, DOI [10.1145/3579639](https://doi.org/10.1145/3579639).

**Original Figshare artefact:** [10.6084/m9.figshare.17425478.v3](https://doi.org/10.6084/m9.figshare.17425478.v3).
