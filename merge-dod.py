#!/usr/bin/env python3

from argparse import ArgumentParser
import json
import re
import sys
import yaml


def read_dod_mappings(dod_file):
    with open(dod_file) as d:
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
    return mapping_by_id


def dod_props_from_mappings(mappings):
    props = []
    for (name, categories) in mappings:
        for category in categories:
            for k, v in category.items():
                props.append({'name': k,
                              'value': v,
                              'class': 'dod-zero-trust-overlay'})
    return props

id_pattern = re.compile(r'\.(\d+)')

def merge_into_control(control, dod_mappings):
    id = control['id'].upper()
    id = id_pattern.sub(r'(\1)', id) # transform e.g. AC-4.1 into AC-4(1)

    if id in dod_mappings:
        mappings = dod_mappings[id]
        control['props'].extend(dod_props_from_mappings(mappings))
    if 'controls' in control:
        for subcontrol in control['controls']:
            merge_into_control(subcontrol, dod_mappings)


def merge_dod_mappings(nist, dod_file):

    dod_mappings = read_dod_mappings(dod_file)

    print(f"Merging {dod_file} ...", file=sys.stderr)

    for group in nist['catalog']['groups']:
        for control in group['controls']:
            merge_into_control(control, dod_mappings)

def main(nist_file, dod_file, sub_file):
    print(f"Reading {nist_file} ...", file=sys.stderr)
    with open(nist_file) as f:
        nist = json.load(f)

    if dod_file:
        merge_dod_mappings(nist, dod_file)
    if sub_file:
        merge_dod_mappings(nist, sub_file)

    print("Writing new JSON ...", file=sys.stderr)
    print(json.dumps(nist))


if __name__ == '__main__':

    parser = ArgumentParser(description='Merge DoD zero trust mappings into NIST controls')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='The NIST controls')
    parser.add_argument('-d', '--dod', type=str, default=None,
                        help='The DoD mappings')
    parser.add_argument('-s', '--sub', type=str, required=True,
                        help='The DoD sub mappings')
    args = parser.parse_args()

    main(args.file, args.dod, args.sub)
