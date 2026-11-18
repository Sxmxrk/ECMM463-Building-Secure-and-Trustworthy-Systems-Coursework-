# Technical report handoff

## Research question

To what extent can the security-misconfiguration results reported by Rahman et al. be reproduced using the released SLI-KUBE implementation and reconstructed historical Kubernetes manifests, and what explains any differences?

## Method

We retrieved the original scanner, expected outputs and URL/metric lists from the Figshare v3 artefact. The dataset contains 2,039 unique manifest paths; 2,031 could be compared with the original scanner's results. We ran 11-category controlled secure/insecure checks, reconstructed historical repository content and compared archived expected values with the scanner at both 13 headline fields and all 20 output fields. We preserved the initial recovery as M07. We then investigated mismatches using Git commit provenance, file sizes and chart-template context, building a separate integrated sensitivity corpus (M08).

## Results

M07 achieved **1,991/2,031 (98.03%)** exact matches on the 13 headline fields and **1,985/2,031 (97.74%)** exact matches over all 20 fields. Nine of eleven category totals already agreed, with the two remaining differences concentrated in hard-coded secrets (172 rather than 219) and HTTP (647 rather than 612). The history analysis associated all 46 full-field mismatches with testable input differences: 39 alternative manifest revisions, four Helm template restorations, and three alternative coherent chart revisions.

M08 combined those changes in an independent source tree, without editing detector rules. Its archived 2,031-row output has **2,031/2,031 (100%)** exact matches across all 20 fields. A strict sensitivity calculation that removes two post-study source substitutions is **2,029/2,031 (99.90%)**.

## Interpretation

The result shows that seemingly minor provenance details—file revision, values content, or the presence of adjacent Helm templates—can materially change scanner output. The stronger contribution is not a perfect score but the ability to trace formerly unexplained differences to independently inspectable source content and replay those contexts under the same detector.

## Limitations

M08 alternatives were chosen *after* examining the published results; this is a sensitivity analysis rather than an unbiased rediscovery of authors' exact original input commits. Two substitutions come from after the study cutoff. The eight original paths not in the comparable set cannot be declared reproduced; `sa-traefik/defaults/pod-privileged.yaml` remains unavailable. The scanner's detections were not independently adjudicated as genuine vulnerabilities.

## Suggested conclusion

The baseline results are highly reproducible within the available source cohort, and the residual differences can be accounted for by source versions and contextual Helm templates. Reproducibility depends as much on preserving input bytes and project context as on releasing detector source code. A versioned, complete dataset snapshot would have made the original study easier to reproduce exactly.

**Cite:** Rahman et al., *Security Misconfigurations in Open Source Kubernetes Manifests: An Empirical Study* (2023), DOI 10.1145/3579639; original dataset and tool, Figshare DOI 10.6084/m9.figshare.17425478.v3.
