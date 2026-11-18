# Ten-minute presentation plan

| Time | Slide | Core message | Visual or evidence |
|---|---|---|---|
| 0:00–0:50 | 1. Research question | Reproduce published SLI-KUBE security-misconfiguration findings | Paper title and Figshare source |
| 0:50–1:45 | 2. What was released | Historical scanner, expected CSVs and 2,039 manifest paths | Simple source-to-scanner diagram |
| 1:45–2:45 | 3. Workflow | Controlled tests, source recovery, M07 comparison, historical investigations, M08 | Five-stage process diagram |
| 2:45–3:45 | 4. Baseline M07 | 98.03% on 13 headline fields; 97.74% on 20 fields | Two KPI figures and cohort count |
| 3:45–4:50 | 5. Why outputs differ | Source revisions alter detected YAML; seven GameOn files explain +35 HTTP findings | Before/after aggregate count |
| 4:50–5:55 | 6. Helm context | Values files require templates; same-commit chart restores secret findings | Values-to-template reference illustration |
| 5:55–7:05 | 7. M08 integrated test | 39 alternate manifests + seven chart contexts; 2,031/2,031 saved output matches | M07 versus M08 comparison |
| 7:05–8:10 | 8. Provenance controls | Commits, dates, blobs, SHA-256 inventory; two post-study sensitivity cases | Selection manifest excerpt with values redacted |
| 8:10–9:10 | 9. Limitations | Missing `sa-traefik`, 8 excluded paths, post hoc selection; 100% is not blind replication | Compact scope table |
| 9:10–10:00 | 10. Takeaway | Versioned inputs and Helm context are essential for reproducibility | One-sentence conclusion |

**Demo option:** Instead of running the complete scanner live, demonstrate `python .\scripts\verify_submission.py`. It finishes quickly and confirms the saved 2,031-file inventory and 40,620 field comparisons. Describe it explicitly as verification of archived outputs, not a live rescan. A short terminal recording of the controlled secure/insecure pairs is also available in the experiment results.

**Speaker guidance:** Avoid claiming that all 2,039 original source paths were fully recovered, that 100% is a held-out accuracy measure, or that the two post-study alternatives are authentic original input snapshots.
