#!/usr/bin/env python3

from argparse import ArgumentParser
import re
import sys
import yaml

ref_id_pattern = re.compile(r'(\w\w-\d+(\(\d+\))?)')

def read_cnswp_mappings(cnswp_file):
    with open(cnswp_file) as c:
        cnswp = yaml.safe_load(c)

    mappings = {}

    for control in cnswp['controls']:
        id = control['id']
        title = control['title']

        ids = []
        new_props = [{'name': 'cnswp-control',
                      'value': f"{id} {title}"}]

        for prop in control['props']:
            name = prop['name']
            value = prop['value']
            if name == 'refs':
                matches = ref_id_pattern.findall(value)
                ids = [m[0] for m in matches]
            elif name == 'zta-tenet':
                new_props.append(prop)

        if not ids:
            print(f"No NIST mapping for {id} {title}", file=sys.stderr)

        for nist_id in ids:
            mappings[nist_id] = new_props

    return mappings

id_pattern = re.compile(r'\.(\d+)')

def merge_into_control(control, cnswp_mappings):
    id = control['id'].upper()
    id = id_pattern.sub(r'(\1)', id)

    if id in cnswp_mappings:
        mappings = cnswp_mappings[id]
        control['props'].extend(mappings)
    if 'controls' in control:
        for subcontrol in control['controls']:
            merge_into_control(subcontrol, cnswp_mappings)

def merge_cnswp_mappings(nist_file, cnswp_file):

    cnswp_mappings = read_cnswp_mappings(cnswp_file)

    print(f"Reading {nist_file} ...", file=sys.stderr)
    with open(nist_file) as f:
        nist = yaml.safe_load(f)

    print(f"Merging {cnswp_file} ...", file=sys.stderr)

    for group in nist['catalog']['groups']:
        for control in group['controls']:
            merge_into_control(control, cnswp_mappings)

    print("Writing new YAML ...", file=sys.stderr)
    print(yaml.dump(nist, sort_keys=False))


if __name__ == '__main__':

    parser = ArgumentParser(description='Merge CNSWP controls into NIST controls')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='The NIST controls')
    parser.add_argument('-c', '--cnswp', type=str, required=True,
                        help='The CNSWP controls')
    args = parser.parse_args()

    merge_cnswp_mappings(args.file, args.cnswp)
