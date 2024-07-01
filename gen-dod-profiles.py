#!/usr/bin/env python3

from argparse import ArgumentParser
import sys
import uuid
import yaml

pillars = ['Enabler', 'User', 'Device', 'Application & Workload', 'Data',
           'Network & Environment', 'Automation & Orchestration',
           'Visibility and Analytics']
mappings = { p: [] for p in pillars }

def get_profile(name, controls):
    profile_uuid = str(uuid.uuid4())
    import_uuid = str(uuid.uuid4())
    profile = {
        'profile': {
            'uuid': profile_uuid,
            'metadata': { 'title': f"NIST SP 800-53 rev5 - DoD pillar {name}" },
            'imports' : [
                {
                    'href': f"#{import_uuid}",
                    'include-controls': [
                        { 'with-ids': controls }
                    ]
                }
            ],
            'back-matter': {
                'resources': [
                    {
                        'uuid': import_uuid,
                        'description': 'NIST SP 800-53 Rev 5.1.1 Controls',
                        'rlinks': [
                            { 'href' : 'NIST_SP-800-53_rev5_catalog.xml' }
                        ]
                    }
                ]
            }
        }
    }
    return profile

def add_mappings(controls):
    for c in controls:
        for p in c['props']:
            if p['name'].startswith('Appendix A'):
                key = p['value']
                mappings[key].append(c['id'])
        if 'controls' in c:
            add_mappings(c['controls'])

def main(filename, prefix):
    print(f"Reading {filename}", file=sys.stderr)
    with open(filename, 'r') as file:
        catalog = yaml.safe_load(file).get('catalog')
        groups = catalog.get('groups')

    for g in groups:
        add_mappings(g['controls'])

    for p in pillars:
        name = f"{prefix}-{p}.yaml"
        print(f"Writing {name}", file=sys.stderr)

        controls = mappings[p]
        profile = get_profile(p, controls)

        with open(name, 'w') as file:
            yaml.dump(profile, file, sort_keys=False)


if __name__ == '__main__':

    parser = ArgumentParser(description='Generate OSCAL profiles for each DoD pillar')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='The DoD annotated NIST controls')
    parser.add_argument('-p', '--prefix', type=str, required=True,
                        help='Filename prefix for generated profiles')
    args = parser.parse_args()
    main(args.file, args.prefix)
