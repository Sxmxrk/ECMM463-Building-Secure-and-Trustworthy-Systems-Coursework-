# Scope, provenance and limitations

## Incomplete original source recovery

The Figshare dataset identifies **2,039** unique file paths, but only **2,031** contribute to the comparable scanner cohort. An `eShopOnContainers` historical `values.yaml` is a verified zero-byte Git blob. The original `softasap/sa-traefik/defaults/pod-privileged.yaml` source has not been recovered. A public 11-line manifest with matching reported scanner fields was identified but has no verified provenance as the authors' file and was **not included** in M07 or M08. Other scan exclusions remain documented in the recovery report; no missing rows were imputed.

## M08 is explanatory, not blind replication

M08's 46 substitutions were selected through access to the expected author counts. This is a *post hoc* source-version and Helm-context sensitivity experiment. It demonstrates that plausible, traceable input contexts can reproduce the archived outcomes, not that the exact original snapshots have been uniquely established. Source files with the same size and scanner outputs may still differ in content.

The two post-study manifest substitutions are marked in `evidence/source_selection.csv`; they must be excluded when claiming historical plausibility under the archive cutoff. Reverting these two yields the calculated 99.90% strict sensitivity figure.

## Environment and implementation

The original paper-era scanner functions were retained. Docker provides the reference environment via `figshare_tool/Dockerfile`; packaged M08 outputs record a separate Python local execution environment. The scanner is dependent on YAML parser/library behaviour and file context. Source metadata, SHA-256 manifests and executable comparison scripts are supplied to help expose any environment-related differences.

## Outcome validity

A scanner agreement rate is not evidence that a manifest is secure, nor is a hard-coded-secret flag proof that a string was an actual credential. The reported 20 fields include operational/status and configuration-presence indicators in addition to the 11 headline security categories. There is no independently adjudicated security ground truth for the entire corpus.

## Research ethics and handling

Historical YAML files may contain credentials, endpoints or insecure defaults as research specimens. Do not deploy them, publish their literal secrets in a report, or use them against external systems. The original GitHub/GitLab and Figshare archives remain credited; local reproduction does not imply endorsement from project maintainers.
