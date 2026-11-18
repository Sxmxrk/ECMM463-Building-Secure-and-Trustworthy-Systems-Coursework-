# Methods

## Aim and reference implementation

The objective was to reproduce the released SLI-KUBE implementation and compare file-level security results with the authors' archived output. The historical scanner shipped with the Figshare v3 release is preserved in `figshare_tool/`. Its security-detection functions are not modified in the comparison experiments. A separate, later KubeSec source release and documented execution patch were used only for the controlled secure/insecure test suite.

## Input corpus

The Figshare records identify 2,039 distinct manifest paths across GitHub and GitLab. Historical recovery reconstructed 2,037 nonempty source files and identified one genuine zero-byte historical Git blob; `sa-traefik/defaults/pod-privileged.yaml` remains unrecovered. The reproducible comparison cohort consists of the 2,031 paths for which the paper-era scanner produced comparable results. The eight paths not in that cohort are not assigned fabricated scanner output.

The source inventory is taken from the authors' URL and metric CSVs in `figshare_source/`. Historical versions were checked against commit identifiers, source-blob hashes and, when appropriate, the manifest line counts recorded by the authors. A line-count match is corroboration, not unique identification of the original blob.

## Experiments

**Controlled tests.** Secure/insecure test pairs exercise 11 misconfiguration categories. Expected outcomes were fixed in advance, and results are preserved in `results/controlled_summary.csv`. Two deliberate false-positive probes and one detector edge-case were recorded as observations, not ground-truth labels.

**M07 — recovered source baseline.** The scanner analysed 2,031 historical manifest files under `experiments/figshare_recovery_M07/`. Its predictions were compared with the authors' archived rows in `results/authors_expected_full_2039.csv`. The original headline agreement covers 13 scalar fields representing the 11 security categories, including separate representations for capability and secret checks. The expanded agreement covers all 20 scanner result fields.

**Source-version investigation.** For all 39 files with content-level disagreements, historical alternative manifest blobs were acquired and scanned using the same paper-era detector. Alternatives were selected after comparing results and were documented by commit, date, Git blob and SHA-256 hashes. Two chosen alternatives are dated after the original historical cutoff, making those two sensitivity-only examples.

**Helm context investigation.** The scanner's `.Values` reference detection depends on adjacent `templates/` directories. Four files were fully resolved by staging the chart templates corresponding to their existing values. Three required chart values and templates from coherent alternative historical commits. The two RabbitMQ values variants used the same 30 June 2019 chart revision, and the skampi archiver used a 21 July 2020 revision. Chart templates are context, not additional benchmark observations.

**M08 — integrated sensitivity run.** The 2,031 M07 observations were copied to a separate frozen directory. Exactly 46 source/context substitutions were applied: 39 alternative manifests, four original-values/pinned-template context cases, and three coherent historical chart cases. Source and chart hashes were checked. The preserved M08 scanner output is compared against the same 2,031 paper rows and all 20 fields.

## Primary endpoint and statistical treatment

A file is an exact match only if all compared fields agree numerically. The study reports both the 13-field headline and 20-field expanded endpoints; neither is a detection-performance measure such as precision or recall against independently adjudicated ground truth. File-level exact agreement and aggregate category counts are reported separately. We do not infer author intent or causality solely from a matching hash, line count or prediction.

All quantitative claims in this package relate to the archived comparable cohort unless explicitly marked otherwise.
