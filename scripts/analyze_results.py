#!/usr/bin/env python3
from pathlib import Path
import argparse
import csv

PAPER_MAP = {
    "Absent Resource Limit": ["NO_RESO"],
    "Absent securityContext": ["NO_SECU_CONTEXT"],
    "Activation of hostIPC": ["TRUE_HOST_IPC"],
    "Activation of hostNetwork": ["TRUE_HOST_NET"],
    "Activation of hostPID": ["TRUE_HOST_PID"],
    "Capability Misuse": ["CAP_SYS_ADMIN", "CAP_SYS_MODULE"],
    "Docker Socket Mounting": ["DOCKERSOCK_PATH"],
    "Escalated Privileges for Child Container Processes": ["ALLOW_PRIVI"],
    "Hard-coded Secret": ["WITHIN_MANIFEST_SECRET", "VALID_TAINT_SECRET"],
    "Insecure HTTP": ["INSECURE_HTTP"],
    "Privileged securityContext": ["SEC_CONT_OVER_PRIVIL"],
}

def as_int(v):
    try:
        return int(float(v or 0))
    except ValueError:
        return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--expectations")
    ap.add_argument("--out")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.csv_path, encoding="latin-1")))
    by_name = {Path(r["YAML_FULL_PATH"]).name: r for r in rows}

    totals = {}
    for category, cols in PAPER_MAP.items():
        totals[category] = sum(sum(as_int(r.get(c)) for c in cols) for r in rows)

    print("\nOriginal 11 paper categories:")
    for k, v in totals.items():
        print(f"{k:52s} {v:>5d}")
    print(f"{'TOTAL (paper-category counts)':52s} {sum(totals.values()):>5d}")

    out_rows = []
    if args.expectations:
        for e in csv.DictReader(open(args.expectations, encoding="utf-8")):
            r = by_name.get(e["file"])
            expected = int(e["expected_count"])
            if r is None:
                actual = ""
                status = "MISSING_ROW"
            else:
                actual = as_int(r.get(e["csv_column"]))
                status = "OBSERVE" if expected < 0 else ("PASS" if actual == expected else "FAIL")
            out_rows.append({
                **e,
                "actual_count": actual,
                "status": status
            })

        print("\nControlled test checks:")
        for r in out_rows:
            print(f"{r['status']:10s} {r['file']:42s} "
                  f"expected={r['expected_count']} actual={r['actual_count']}")

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        fields = list(out_rows[0].keys()) if out_rows else ["category", "count"]
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            if out_rows:
                w.writerows(out_rows)
            else:
                for category, count in totals.items():
                    w.writerow({"category": category, "count": count})
        print(f"\nWrote {out}")

if __name__ == "__main__":
    main()
