#!/usr/bin/env python3
"""Rebuild the frozen M08 corpus from M07 and immutable source evidence.

A new output directory is required. The M07 and distributed M08 trees are read-only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from pathlib import Path


def rows(file: Path):
    with file.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def digest(file: Path):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def safe(root: Path, rel: str) -> Path:
    value = Path(rel.replace('\\', '/'))
    if value.is_absolute() or '..' in value.parts or not value.parts:
        raise ValueError('Invalid relative path: ' + rel)
    return root / value


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--out', default='experiments/figshare_recovery_M08_rebuilt',
                    help='New, package-relative dataset folder (must not exist)')
    action = ap.add_mutually_exclusive_group(required=True)
    action.add_argument('--plan', action='store_true')
    action.add_argument('--build', action='store_true')
    args = ap.parse_args()
    root = args.root.resolve()
    original = root / 'experiments/figshare_recovery_M07'
    published = root / 'experiments/figshare_recovery_M08'
    output = safe(root, args.out)
    if output.resolve() in (original.resolve(), published.resolve()):
        raise RuntimeError('Refusing to replace a published experiment')
    if output.exists():
        raise FileExistsError('Output exists; refusing to overwrite: ' + str(output))
    selected = rows(root / 'evidence/source_selection.csv')
    templates = rows(root / 'evidence/template_additions.csv')
    inventory = rows(root / 'results/figshare_M08_manifest_inventory.csv')
    assert len(selected) == 46 and len(templates) == 51 and len(inventory) == 2031
    for item in selected:
        m07 = safe(original / item['source'], item['relative_path'])
        candidate = safe(root, item['evidence_path'])
        assert digest(m07) == item['m07_sha256'], item['relative_path']
        assert digest(candidate) == item['m08_sha256'], item['relative_path']
    for item in templates:
        assert digest(safe(root / 'evidence/template_additions', item['relative_path'])) == item['sha256']
    print(f'M07 input: {original}')
    print(f'New M08 output: {output}')
    print(f'Selections verified: {len(selected)}; additional templates verified: {len(templates)}')
    if args.plan:
        print('Plan complete. No files written.')
        return
    try:
        shutil.copytree(original, output, ignore=shutil.ignore_patterns('slikube_figshare_results.csv'))
        for item in selected:
            from_file = safe(root, item['evidence_path'])
            to_file = safe(output / item['source'], item['relative_path'])
            to_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(from_file, to_file)
        for item in templates:
            from_file = safe(root / 'evidence/template_additions', item['relative_path'])
            to_file = safe(output, item['relative_path'])
            if to_file.exists():
                raise RuntimeError('Template was already present: ' + item['relative_path'])
            to_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(from_file, to_file)
        expected_files = {r['source'] + '/' + r['relative_path']: r['m08_sha256'] for r in inventory}
        # M07 also retains seven source files outside the 2,031 comparable rows.
        # Preserve them byte-for-byte; they are not benchmark observations.
        for original_file in original.rglob('*'):
            if not original_file.is_file() or original_file.name == 'slikube_figshare_results.csv':
                continue
            name = str(original_file.relative_to(original)).replace('\\', '/')
            if name not in expected_files:
                expected_files[name] = digest(original_file)
        expected_files.update({r['relative_path']: r['sha256'] for r in templates})
        actual_files = {str(p.relative_to(output)).replace('\\', '/') for p in output.rglob('*') if p.is_file()}
        assert actual_files == set(expected_files), (len(actual_files), len(expected_files))
        for name, sha in expected_files.items():
            assert digest(safe(output, name)) == sha, name
        published_files = {str(p.relative_to(published)).replace('\\', '/') for p in published.rglob('*') if p.is_file()}
        assert actual_files == published_files
        print(f'PASS — Rebuilt {len(actual_files)} files, byte-for-byte identical to the published M08')
        print('M07 and the distributed M08 were not modified.')
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise


if __name__ == '__main__':
    main()
