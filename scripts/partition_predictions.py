#!/usr/bin/env python3
import argparse
import json
import os
import sys

GROUPS = {
    'django': ['django'],
    'sympy': ['sympy'],
    'viz-docs': ['matplotlib', 'sphinx-doc'],
    'core-libs': ['scikit-learn', 'astropy', 'pytest-dev'],
    'utils-web': ['pydata', 'pylint-dev', 'psf', 'mwaskom', 'pallets']
}

def main():
    parser = argparse.ArgumentParser(description="Partition predictions.jsonl by matrix group")
    parser.add_argument('--input', default='predictions.jsonl', help='Path to master predictions.jsonl')
    parser.add_argument('--group', required=True, choices=list(GROUPS.keys()) + ['all'], help='Matrix group name')
    parser.add_argument('--output', required=True, help='Output partitioned jsonl file')
    args = parser.parse_args()

    target_repos = None if args.group == 'all' else GROUPS[args.group]
    matched = 0
    total = 0

    with open(args.input, 'r', encoding='utf-8') as f_in, open(args.output, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            total += 1
            repo = d['instance_id'].split('__')[0]
            if target_repos is None or any(repo.startswith(r) for r in target_repos):
                f_out.write(json.dumps(d) + '\n')
                matched += 1

    print(f"[Partition] Group: {args.group} | Matched: {matched}/{total} instances -> {args.output}")

if __name__ == '__main__':
    main()
