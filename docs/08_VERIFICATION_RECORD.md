# Verification record

**Release audit date:** 10 November 2026  
**Unit of comparison:** one file with 20 numeric scanner output fields

## Completed checks

| Test | Result |
|---|---|
| Compared 2,031 saved scanner-output rows against the authors' 20 archived fields | 40,620 of 40,620 equal |
| Matched the M07 13-field headline figure to archived results | 1,991/2,031 |
| Matched the M07 20-field figure to archived results | 1,985/2,031 |
| Verified the M08 SHA-256 file inventory | 2,031 of 2,031 |
| Checked alternative sources and chart contexts | 46 selections; 51 template additions |
| Checked integrity of alternative candidate Git blobs | 46 of 46 |
| Rebuilt M08 from M07 and compact evidence in an independent output tree | 2,089 of 2,089 files byte-identical |
| Rescanned selected M08 examples with original detector functions | 15 of 15 files matched across 20 fields |

## Execution scope

The complete M08 output archived in `results/figshare_M08_scanner_output.csv` contains 2,031 evaluations. The release audit independently validated all saved rows and hashes. The locally available scanner dependencies were sufficient for a 15-file functional smoke test. A separate full rescan was attempted but was not completed under the packaging environment's runtime limit; this is not represented as an additional full detector run.

Docker was not available in the packaging environment. The included `scripts/run_m08.ps1` provides a non-destructive way to perform the full Python 3.10/Docker reproduction on Windows, writing to `results/verification_run/`.

Absolute paths in saved scanner CSVs are execution-time metadata, not file lookup requirements. Verification indexes observations using their repository-relative `github/` or `gitlab/` suffixes.

**Interpretation:** passing a hash/CSV audit establishes archive integrity and numerical consistency. It is not an independent estimate of scanner accuracy, and the historically selected M08 sources are not held-out test inputs.
