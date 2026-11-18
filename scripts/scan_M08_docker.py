#!/usr/bin/env python3
"""Integrated 20-field M08 evaluation using the unchanged 2021 scanner functions.

This runner evaluates the same 2,031 manifests processed by M07, now in a
separate M08 source tree with pre-verified alternative files and chart context.
Template files provide context but are NOT additional benchmark observations.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import platform
import sys
from collections import Counter
from pathlib import Path

FIELDS = [
    'WITHIN_MANIFEST_SECRET', 'VALID_TAINT_SECRET', 'SEC_CONT_OVER_PRIVIL',
    'INSECURE_HTTP', 'NO_SECU_CONTEXT', 'NO_DEFAULT_NSPACE', 'NO_RESO',
    'NO_ROLLING_UPDATE', 'NO_NETWORK_POLICY', 'TRUE_HOST_PID', 'TRUE_HOST_IPC',
    'DOCKERSOCK_PATH', 'TRUE_HOST_NET', 'CAP_SYS_ADMIN', 'HOST_ALIAS',
    'ALLOW_PRIVI', 'SECCOMP_UNCONFINED', 'CAP_SYS_MODULE',
    'K8S_STATUS', 'HELM_STATUS',
]
HEADLINE13 = [
    'WITHIN_MANIFEST_SECRET', 'VALID_TAINT_SECRET', 'SEC_CONT_OVER_PRIVIL',
    'INSECURE_HTTP', 'NO_SECU_CONTEXT', 'NO_RESO', 'TRUE_HOST_PID',
    'TRUE_HOST_IPC', 'DOCKERSOCK_PATH', 'TRUE_HOST_NET', 'CAP_SYS_ADMIN',
    'ALLOW_PRIVI', 'CAP_SYS_MODULE',
]


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path, data, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns)
        w.writeheader();w.writerows(data)


def as_int(value):
    if isinstance(value, bool):
        return int(value)
    if str(value).strip().lower() in ('true', 'false'):
        return int(str(value).strip().lower() == 'true')
    return int(value)


def key_from_m07(path):
    path=str(path).replace('\\','/')
    for source in ('github','gitlab'):
        mark='/'+source+'/'
        if mark in path:
            return source,path.split(mark,1)[1]
    raise RuntimeError('M07 scanner path has no dataset source: '+path)


def full20(path, scanner, parser):
    filename=str(path)
    raw=scanner.scanSingleManifest(filename)
    values=[
        sum(len(group) for group in raw[0]), len(raw[2]), len(raw[3]),
        len(scanner.scanForHTTP(filename)),
        len(scanner.scanForMissingSecurityContext(filename)),
        len(scanner.scanForDefaultNamespace(filename)),
        len(scanner.scanForResourceLimits(filename)),
        len(scanner.scanForRollingUpdates(filename)),
        len(scanner.scanForMissingNetworkPolicy(filename)),
        len(scanner.scanForTruePID(filename)),
        len(scanner.scanForTrueIPC(filename)),
        len(scanner.scanDockerSock(filename)),
        len(scanner.scanForHostNetwork(filename)),
        len(scanner.scanForCAPSYS(filename)),
        len(scanner.scanForHostAliases(filename)),
        len(scanner.scanAllowPrivileges(filename)),
        len(scanner.scanForUnconfinedSeccomp(filename)),
        len(scanner.scanForCAPMODULE(filename)),
        parser.checkIfValidK8SYaml(filename),
        parser.checkIfValidHelm(filename),
    ]
    if len(values) != 20:
        raise RuntimeError('Scanner result schema changed')
    return dict(zip(FIELDS,[as_int(v) for v in values]))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path('/project'))
    ap.add_argument('--out',type=Path,default=Path('/results'))
    ap.add_argument('--smoke',action='store_true',help='Scan a selection only; do not write official M08 outputs')
    ap.add_argument('--limit',type=int,default=12,help='Maximum sample rows with --smoke')
    args=ap.parse_args()
    root=args.root.resolve()
    out=args.out.resolve()
    stage=root/'experiments/figshare_recovery_M08'
    original=root/'experiments/figshare_recovery_M07'
    required=[
        original/'slikube_figshare_results.csv',
        root/'results/authors_expected_full_2039.csv',
        root/'results/figshare_recovery_M07_all20_per_file.csv',
        root/'results/figshare_M08_selection_manifest.csv',
        root/'results/figshare_M08_manifest_inventory.csv',
    ]
    for p in required:
        if not p.is_file():
            raise FileNotFoundError(p)
    if not stage.is_dir():
        raise FileNotFoundError(stage)
    m07_rows=read_csv(required[0]); author_rows=read_csv(required[1]); audit_rows=read_csv(required[2])
    selection=read_csv(required[3]); inventory=read_csv(required[4])
    m07={key_from_m07(r['YAML_FULL_PATH']):r for r in m07_rows}
    authors={(r['SOURCE'].lower(),r['RELATIVE_PATH'].replace('\\','/')):r for r in author_rows}
    audit={(r['source'],r['relative_path']):r for r in audit_rows}
    changed={(r['source'],r['relative_path']):r for r in selection}
    stored={(r['source'],r['relative_path']):r for r in inventory}
    if not (len(m07)==len(audit)==len(stored)==2031 and len(changed)==46
            and set(m07)==set(audit)==set(stored) and set(changed)<set(m07)):
        raise RuntimeError('M08 roster does not match the verified 2,031-row M07 experiment')
    if any(str(audit[k]['exact_all20']).lower() != ('false' if k in changed else 'true') for k in m07):
        raise RuntimeError('M08 selections are not precisely the 46 original mismatches')
    for source,rel in m07:
        p=stage/source/Path(rel)
        if not p.is_file():
            raise FileNotFoundError('M08 manifest missing: '+str(p))
        if hashlib.sha256(p.read_bytes()).hexdigest()!=stored[(source,rel)]['m08_sha256']:
            raise RuntimeError('M08 manifest integrity mismatch: '+rel)
    if args.smoke:
        # Include Helm variants and source-only alternatives to validate distinct code paths.
        order=[]
        for group in ('helm_historical_chart','helm_original_context','historical_manifest'):
            order.extend(k for k,v in sorted(changed.items()) if v['resolution']==group)
        order += sorted(k for k in m07 if k not in changed)
        keys=order[:args.limit]
        print('Smoke test only: ',len(keys),'of',len(m07),'files. No official reports will be written.',flush=True)
    else:
        keys=sorted(m07)
        if (out/'figshare_M08_full20_per_file.csv').exists():
            raise RuntimeError('M08 results already exist. Refusing to overwrite them.')
        print('Integrated M08 scan:',len(keys),'original M07 observations; 46 verified substitutions.',flush=True)

    # In Docker, /app holds the exact paper-era scanner source. Local fallback
    # is provided for portability; Docker is the reference execution environment.
    scanner_dir=Path('/app') if Path('/app/scanner.py').is_file() else root/'figshare_tool'
    sys.path.insert(0,str(scanner_dir))
    import scanner
    import parser
    import numpy
    import yaml
    per=[]; actual=[]; aggregate_author=Counter();aggregate_m08=Counter();aggregate_m07=Counter()
    error_rows=[]
    for idx,(source,rel) in enumerate(keys,1):
        path=stage/source/Path(rel)
        expected={f:as_int(authors[(source,rel)][f]) for f in FIELDS}
        previous={f:as_int(m07[(source,rel)][f]) for f in FIELDS}
        try:
            got=full20(path,scanner,parser)
        except Exception as exc:
            error_rows.append({'source':source,'relative_path':rel,'error_class':type(exc).__name__,
                               'error_summary':str(exc)[:240]})
            print('FAILED '+source+'/'+rel+': '+str(exc)[:100],flush=True)
            continue
        mismatch=[f for f in FIELDS if got[f] != expected[f]]
        changed_fields=[f for f in FIELDS if got[f] != previous[f]]
        per.append(dict(source=source,relative_path=rel,
            resolution=changed.get((source,rel),{}).get('resolution','unchanged'),
            candidate_commit=changed.get((source,rel),{}).get('commit',''),
            post_study=changed.get((source,rel),{}).get('post_study','False'),
            exact_headline13=not any(f in HEADLINE13 for f in mismatch),
            exact_all20=not mismatch,
            field_mismatches=';'.join(mismatch),field_changes_from_M07=';'.join(changed_fields),
            mismatch_count=len(mismatch)))
        actual.append(dict(DIR=str(stage),YAML_FULL_PATH=str(path),**got))
        for f in FIELDS:
            aggregate_author[f]+=expected[f]
            aggregate_m08[f]+=got[f]
            aggregate_m07[f]+=previous[f]
        if args.smoke or (idx % 100 == 0) or mismatch:
            print(f'[{idx}/{len(keys)}] {source}/{rel}: '+('MATCH' if not mismatch else 'DIFF '+','.join(mismatch)),flush=True)
    if args.smoke:
        if error_rows:
            raise RuntimeError(f'{len(error_rows)} smoke-test scan errors')
        if any(not r['exact_all20'] for r in per):
            raise RuntimeError('Smoke-test mismatch: '+repr([r['relative_path'] for r in per if not r['exact_all20']]))
        print('Smoke test passed:',len(per),'/',len(per),'files, all 20 fields',flush=True)
        return
    if error_rows:
        write_csv(out/'figshare_M08_scan_errors.csv',error_rows,list(error_rows[0]))
        raise RuntimeError('M08 scan failed for '+str(len(error_rows))+' files. No completed comparison was written.')
    if len(per)!=2031 or len(actual)!=2031:
        raise RuntimeError('M08 scan row count is incomplete')
    old_head=sum(all(as_int(m07[k][f])==as_int(authors[k][f]) for f in HEADLINE13) for k in m07)
    old_full=sum(all(as_int(m07[k][f])==as_int(authors[k][f]) for f in FIELDS) for k in m07)
    good13=sum(r['exact_headline13'] for r in per)
    good20=sum(r['exact_all20'] for r in per)
    baseline_regressions=[r for r in per if r['resolution']=='unchanged' and not r['exact_all20']]
    poststudy=[r for r in per if str(r['post_study']).lower()=='true']
    # Strict sensitivity substitutes back the original pinned rows for the two
    # post-study candidates; other proven alternatives remain in place.
    strict_matches=good20-sum(r['exact_all20'] for r in poststudy)+sum(
        all(as_int(m07[(r['source'],r['relative_path'])][f])==as_int(authors[(r['source'],r['relative_path'])][f]) for f in FIELDS)
        for r in poststudy)
    stats=[
        ('authors_manifest_paths',len(authors)),
        ('M07_comparable_files',len(m07)),
        ('M07_exact_headline13',old_head),
        ('M07_exact_all20',old_full),
        ('M08_scanned_files',len(per)),
        ('M08_selected_alternative_files',len(changed)),
        ('M08_exact_headline13',good13),
        ('M08_exact_all20',good20),
        ('M08_exact_all20_percent',f'{100*good20/len(per):.4f}'),
        ('M08_strict_pre_study_sensitivity_exact_all20',strict_matches),
        ('post_study_source_alternatives',len(poststudy)),
        ('M08_unexpected_unchanged_file_mismatches',len(baseline_regressions)),
        ('scanner_source',str(scanner_dir)),
        ('python_version',platform.python_version()),
        ('numpy_version',numpy.__version__),
        ('pyyaml_version',yaml.__version__),
    ]
    for f in FIELDS:
        stats.extend([('authors_sum_'+f,aggregate_author[f]),('M07_sum_'+f,aggregate_m07[f]),('M08_sum_'+f,aggregate_m08[f])])
    write_csv(out/'figshare_M08_scanner_output.csv',actual,['DIR','YAML_FULL_PATH']+FIELDS)
    write_csv(out/'figshare_M08_full20_per_file.csv',per,list(per[0]))
    write_csv(out/'figshare_M08_summary.csv',[dict(metric=a,value=b) for a,b in stats],['metric','value'])
    print('M07 full20:',old_full,'/',len(per),flush=True)
    print('M08 full20:',good20,'/',len(per),flush=True)
    print('M08 headline13:',good13,'/',len(per),flush=True)
    print('Strict pre-study sensitivity:',strict_matches,'/',len(per),flush=True)
    print('Unchanged baseline regressions:',len(baseline_regressions),flush=True)
    print('Results saved in '+str(out),flush=True)
    if good20 != len(per) or baseline_regressions:
        raise RuntimeError('Integrated M08 scan did not match all authors fields; inspect M08 per-file report')

if __name__ == '__main__':
    main()
