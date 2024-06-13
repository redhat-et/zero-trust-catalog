#!/usr/bin/env python3

from argparse import ArgumentParser
import yaml


if __name__ == '__main__':

    parser = ArgumentParser(description='Merge DoD zero trust mappings into NIST controls')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='The NIST controls')
    parser.add_argument('-d', '--dod', type=str, required=True,
                        help='The DoD mappings')
    args = parser.parse_args()

    with open(args.dod) as d:
        dod = yaml.safe_load(d)
    mapping_by_id = {}
    for section in dod:
        name = section['name']
        for m in section['mappings']:
            key = m['key']
            categories = m['categories']
            if key not in mapping_by_id:
                mapping_by_id[key] = []
            mapping_by_id[key].append((name, categories))

    with open(args.file) as f:
        nist = yaml.safe_load(f)

    for group in nist['catalog']['groups']:
        for control in group['controls']:
            id = control['id'].upper()
            if id in mapping_by_id:
                mapping = mapping_by_id[id]
                control['props'].append({'class': 'dod-zero-trust-overlay'})

    print(yaml.dump(nist))
