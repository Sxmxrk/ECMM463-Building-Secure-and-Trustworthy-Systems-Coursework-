# Results

## Summary

| Measure | M07 | M08 |
|---|---:|---:|
| Comparable file count | 2,031 | 2,031 |
| 13 headline fields: exact matches | 1,991 | 2,031 |
| 13 headline fields: agreement | 98.03% | 100.00% |
| 20 output fields: exact matches | 1,985 | 2,031 |
| 20 output fields: agreement | 97.74% | 100.00% |
| Files differing on at least one of 20 fields | 46 | 0 |

M08 is a **historical-source sensitivity analysis**. Its 100% agreement should not be described as blind replication or as a correction to M07. The source candidates were evaluated using the archived author outcomes.

## Discrepancy reconciliation

| Mechanism | Files explained |
|---|---:|
| Alternative manifest revisions | 39 |
| Restored Helm templates with the original values | 4 |
| Alternative coherent historical Helm charts | 3 |
| **Total previously mismatching files** | **46** |

The 39 alternative-manifest cases include GitHub and GitLab projects with versions whose file sizes and scanner outputs align with the archive. Seven GameOn files accounted for **35 extra HTTP findings in M07**; their historical replacements all agree with the authors. Other projects include Kubernetes-native-testbed (seven files), Java MicroProfile (five), Spring Cloud Data Flow (six), Emissary, RSO and smaller services.

For Helm findings, the M07 scan included no accompanying chart template context for some values files, yielding a deficit of 43 `VALID_TAINT_SECRET` occurrences. Historical context restored 35 of these in seven values files, with exact file-level outcomes for four. Coherent chart versions then matched the other three files, eliminating the remaining eight findings.

## Aggregate results for the 11 paper security categories

| Category | Authors / M08 | M07 |
|---|---:|---:|
| Absent resource limit | 79 | 79 |
| Absent `securityContext` | 83 | 83 |
| hostIPC enabled | 1 | 1 |
| hostNetwork enabled | 14 | 14 |
| hostPID enabled | 5 | 5 |
| Capability misuse | 20 | 20 |
| Docker socket mounting | 4 | 4 |
| Privilege escalation allowed | 3 | 3 |
| Hard-coded secret | 219 | 172 |
| Insecure HTTP | 612 | 647 |
| Privileged container `securityContext` | 9 | 9 |
| **Total** | **1,049** | **1,037** |

The hard-coded-secret category consists of the separate within-manifest and Helm-taint fields. The capability-misuse category combines two scanner capability flags. These category totals are for the 2,031 comparable files, not the 2,039-source archive as a whole.

## Sensitivity boundaries

The fully matched M08 configuration uses two source revisions committed after the historical cutoff. Reverting those two to their M07 files while retaining other substitutions gives a calculated **2,029 / 2,031 (99.90%)** 20-field match rate. This stricter figure is a sensitivity calculation, not a separately executed integrated scan.

The M08 CSV reports a complete 2,031-row scanner run. This release has been checked row-by-row against all 20 author fields and its manifest inventory hashes; selected files have also been rescanned independently. An independent packaging audit checked 15 representative files with the original scanner; a complete fresh scanner rerun is available through the Docker procedure and should be distinguished from verification of the supplied results.
