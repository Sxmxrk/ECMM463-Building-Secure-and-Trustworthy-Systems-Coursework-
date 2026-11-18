#!/usr/bin/env python3
"""Verify archived scanner observations, source provenance and M08 integrity.

This is an offline evidence audit, not a fresh invocation of the detector.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path

FIELDS = (
    'WITHIN_MANIFEST_SECRET', 'VALID_TAINT_SECRET', 'SEC_CONT_OVER_PRIVIL',
    'INSECURE_HTTP', 'NO_SECU_CONTEXT', 'NO_DEFAULT_NSPACE', 'NO_RESO',
    'NO_ROLLING_UPDATE', 'NO_NETWORK_POLICY', 'TRUE_HOST_PID', 'TRUE_HOST_IPC',
    'DOCKERSOCK_PATH', 'TRUE_HOST_NET', 'CAP_SYS_ADMIN', 'HOST_ALIAS',
    'ALLOW_PRIVI', 'SECCOMP_UNCONFINED', 'CAP_SYS_MODULE',
    'K8S_STATUS', 'HELM_STATUS',
)
HEADLINE13 = tuple(k for k in FIELDS if k not in {
    'NO_DEFAULT_NSPACE', 'NO_ROLLING_UPDATE', 'NO_NETWORK_POLICY',
    'HOST_ALIAS', 'SECCOMP_UNCONFINED', 'K8S_STATUS', 'HELM_STATUS',
})


def read_csv(file: Path) -> list[dict[str, str]]:
    with file.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def safe(root: Path, value: str) -> Path:
    subpath = Path(value.replace('\\', '/'))
    if subpath.is_absolute() or '..' in subpath.parts or not subpath.parts:
        raise ValueError('Unsafe repository-relative path: ' + value)
    return root / subpath


def digest(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()


def git_blob(file: Path) -> str:
    content = file.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()


def as_int(value: str) -> int:
    text = str(value).strip().lower()
    if text in ('true', 'false'):
        return int(text == 'true')
    return int(text)


def index(rows: list[dict], x: str = 'source', y: str = 'relative_path') -> dict[tuple[str, str], dict]:
    output = {}
    for row in rows:
        key = (row[x].lower(), row[y].replace('\\', '/'))
        if key in output:
            raise AssertionError('Duplicate row: ' + repr(key))
        output[key] = row
    return output


def scanner_rows(rows: list[dict]) -> dict[tuple[str, str], dict]:
    output = {}
    for row in rows:
        path = row['YAML_FULL_PATH'].replace('\\', '/')
        for source in ('github', 'gitlab'):
            marker = '/' + source + '/'
            if marker in path:
                key = (source, path.split(marker, 1)[1])
                break
        else:
            raise AssertionError('Scanner result path lacks source delimiter: ' + path)
        if key in output:
            raise AssertionError('Duplicate scanner path: ' + repr(key))
        output[key] = row
    return output


def verify(root: Path) -> None:
    results = root / 'results'
    dataset7 = root / 'experiments/figshare_recovery_M07'
    dataset8 = root / 'experiments/figshare_recovery_M08'
    expected = index(read_csv(results / 'authors_expected_full_2039.csv'), 'SOURCE', 'RELATIVE_PATH')
    seven = scanner_rows(read_csv(dataset7 / 'slikube_figshare_results.csv'))
    eight = scanner_rows(read_csv(results / 'figshare_M08_scanner_output.csv'))
    audit7 = index(read_csv(results / 'figshare_recovery_M07_all20_per_file.csv'))
    audit8 = index(read_csv(results / 'figshare_M08_full20_per_file.csv'))
    inventory = index(read_csv(results / 'figshare_M08_manifest_inventory.csv'))
    selection = index(read_csv(root / 'evidence/source_selection.csv'))
    templates = read_csv(root / 'evidence/template_additions.csv')
    assert len(expected) == 2039, 'Expected 2,039 author rows'
    assert len(seven) == len(eight) == len(audit7) == len(audit8) == len(inventory) == 2031
    assert set(seven) == set(eight) == set(audit7) == set(audit8) == set(inventory)
    assert set(seven) <= set(expected)
    assert len(selection) == 46
    assert set(selection) == {k for k in audit7 if str(audit7[k]['exact_all20']).lower() == 'false'}
    assert len(templates) == 51

    correct7 = correct7_head = correct8 = correct8_head = 0
    changes = Counter()
    post_study = 0
    for key in sorted(seven):
        source, relative_path = key
        authors = expected[key]
        m7 = seven[key]
        m8 = eight[key]
        good7 = all(as_int(m7[f]) == as_int(authors[f]) for f in FIELDS)
        good7_head = all(as_int(m7[f]) == as_int(authors[f]) for f in HEADLINE13)
        good8 = all(as_int(m8[f]) == as_int(authors[f]) for f in FIELDS)
        good8_head = all(as_int(m8[f]) == as_int(authors[f]) for f in HEADLINE13)
        assert str(audit7[key]['exact_all20']).lower() == str(good7).lower(), key
        assert str(audit8[key]['exact_all20']).lower() == str(good8).lower(), key
        correct7 += good7
        correct7_head += good7_head
        correct8 += good8
        correct8_head += good8_head
        m08file = safe(dataset8 / source, relative_path)
        assert m08file.is_file(), str(m08file)
        assert digest(m08file) == inventory[key]['m08_sha256'], relative_path
        if key in selection:
            selected = selection[key]
            m07file = safe(dataset7 / source, relative_path)
            evidence = safe(root, selected['evidence_path'])
            assert m07file.is_file() and evidence.is_file()
            assert digest(m07file) == selected['m07_sha256'], relative_path
            assert digest(evidence) == selected['m08_sha256'], relative_path
            assert digest(m08file) == selected['m08_sha256'], relative_path
            assert git_blob(evidence) == selected['git_blob'], relative_path
            changes[selected['resolution']] += 1
            post_study += str(selected['post_study']).lower() == 'true'
        else:
            assert inventory[key]['changed_source_or_context'].lower() == 'false'
            assert digest(safe(dataset7 / source, relative_path)) == digest(m08file), relative_path

    expected_changes = {'historical_manifest': 39,
                        'helm_original_context': 4,
                        'helm_historical_chart': 3}
    assert dict(changes) == expected_changes, changes
    assert post_study == 2
    assert (correct7_head, correct7, correct8_head, correct8) == (1991, 1985, 2031, 2031)
    archive7 = {p.relative_to(dataset7).as_posix() for p in dataset7.rglob('*') if p.is_file()}
    archive8 = {p.relative_to(dataset8).as_posix() for p in dataset8.rglob('*') if p.is_file()}
    add_names = {r['relative_path'] for r in templates}
    assert len(add_names) == 51 and archive8 - archive7 == add_names
    assert archive7 - archive8 == {'slikube_figshare_results.csv'}
    for row in templates:
        rel = row['relative_path']
        assert '/templates/' in rel
        archive_file = safe(dataset8, rel)
        evidence_file = safe(root / 'evidence/template_additions', rel)
        assert digest(archive_file) == digest(evidence_file) == row['sha256'], rel
    summary = {r['metric']: r['value'] for r in read_csv(results / 'figshare_M08_summary.csv')}
    assert as_int(summary['M07_exact_headline13']) == correct7_head
    assert as_int(summary['M07_exact_all20']) == correct7
    assert as_int(summary['M08_exact_headline13']) == correct8_head
    assert as_int(summary['M08_exact_all20']) == correct8
    assert as_int(summary['M08_strict_pre_study_sensitivity_exact_all20']) == 2029

    print('PASS — Archive and reported results are internally consistent')
    print(f'  Figshare paths:              {len(expected)}')
    print(f'  Comparable files:            {len(eight)}')
    print(f'  M07 headline (13 fields):    {correct7_head}/{len(seven)}')
    print(f'  M07 full output (20 fields): {correct7}/{len(seven)}')
    print(f'  M08 full output (20 fields): {correct8}/{len(eight)}')
    print(f'  Source/context alternatives: {len(selection)} (39 manifests, 7 Helm cases)')
    print(f'  Added historical templates: {len(templates)}')
    print(f'  Post-study alternatives:     {post_study}')
    print(f'  SHA-256 verified manifests:  {len(eight)}')
    print(f'  Author-field comparisons:    {len(eight)*len(FIELDS):,}')
    print('  This is a saved-output integrity audit, not a new scanner run.')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    verify(args.root.resolve())


if __name__ == '__main__':
    main()
