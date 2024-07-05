#!/usr/bin/env python3

from argparse import ArgumentParser, BooleanOptionalAction
import json
import sys
import uuid
import yaml

pillars = ['Enabler', 'User', 'Device', 'Application & Workload', 'Data',
           'Network & Environment', 'Automation & Orchestration',
           'Visibility and Analytics']
mappings = { p: [] for p in pillars }
controls_by_id = { }
baselines_by_name = { }
seen_ids = { }

profile_uuid = str(uuid.uuid4())
import_uuid = str(uuid.uuid4())

html_preamble = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body>
'''

html_postamble = '''<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
</html>
'''

def get_profile(name, controls):
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

def get_catalog(name, ids):

    catalog = {
        'catalog': {
            'uuid': profile_uuid,
            'metadata': { 'title': f"NIST SP 800-53 rev5 - DoD pillar {name}" },
            'controls': [controls_by_id[id] for id in ids]
        }
    }

    return catalog

def add_mappings(controls):
    for c in controls:
        controls_by_id[c['id']] = c
        for p in c['props']:
            if p['name'].startswith('Appendix A'):
                key = p['value']
                mappings[key].append(c['id'])
        if 'controls' in c:
            add_mappings(c['controls'])

def load_baseline(filename):
    ids = []
    with open(filename, 'r') as file:
        profile = yaml.safe_load(file).get('profile')

    for i in profile['imports']:
        for inc in i['include-controls']:
            for id in inc['with-ids']:
                if id not in seen_ids:
                    ids.append(id)
                    seen_ids[id] = id

    return ids

def write_profile(name, prefix, controls, resolve=False):
    filename = f"{prefix}-{name}.yaml"
    print(f"Writing {filename}", file=sys.stderr)

    if resolve:
        content = get_catalog(name, controls)
    else:
        content = get_profile(name, controls)

    with open(filename, 'w') as file:
        yaml.dump(content, file, sort_keys=False)

styles = ['primary', 'success', 'danger']
headings = ['Low', 'Moderate', 'High']

def generate_html():
    html = []

    html.append('<div class="container-fluid" style="padding: 1em;">')
    html.append('<header class="border-bottom d-flex justify-content-center">')
    html.append('<h3>NIST SP 800-53 rev5 Controls by DoD pillar and NIST baseline</h3>')
    html.append('</header>')
    html.append('</div>')

    html.append('<div class="container-fluid">')
    html.append('<div class="row align-items-end">')
    html.append('  <div class="col"></div>')
    for p in pillars:
        html.append('  <div class="col">')
        html.append(f'    <h5>{p}</h5>')
        html.append('  </div>')
    html.append('</div>')

    for i, k in reversed(list(enumerate(baselines_by_name.keys()))):
        style = styles[i]
        head = headings[i]
        classes = f'badge bg-{style}-subtle text-{style}'

        baseline_ids = { id : id for id in baselines_by_name[k] }

        html.append('<div class="row align-items-start">')
        html.append('  <div class="col">')
        html.append(f'    <h5>{head} Baseline</h5>')
        html.append('  </div>')

        for p in pillars:
            html.append('  <div class="col">')

            for id in mappings[p]:
                if id in baseline_ids:
                    html.append(f'    <span class="{classes}">{id}</span>')

            html.append('  </div>')

        html.append('</div>')

    html.append('</div>')

    return "\n".join(html)

def main(filename, prefix, baselines, resolve=False, visualize=False):

    for b in baselines:
        ids = load_baseline(b)
        baselines_by_name[b] = ids

    print(f"Reading {filename}", file=sys.stderr)
    with open(filename, 'r') as file:
        catalog = json.load(file).get('catalog')
        groups = catalog.get('groups')

    for g in groups:
        add_mappings(g['controls'])

    if visualize:
        print('Generating HTML', file=sys.stderr)
        print(html_preamble)
        print(generate_html())
        print(html_postamble)
    else:
        for p in pillars:
            controls = mappings[p]
            write_profile(p, prefix, controls, resolve)

if __name__ == '__main__':

    parser = ArgumentParser(description='Generate OSCAL profiles for each DoD pillar')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='The DoD annotated NIST controls')
    parser.add_argument('-p', '--prefix', type=str, default='dod-profile',
                        help='Filename prefix for generated profiles')
    parser.add_argument('-r', '--resolve', action=BooleanOptionalAction,
                        help='Include control definitions inline, not just as imports')
    parser.add_argument('-b', '--baseline', type=str, action='append',
                        help='Include NIST baseline information')
    parser.add_argument('-V', '--visualize', action=BooleanOptionalAction,
                        help='Generate a visualization of controls by pillar')
    args = parser.parse_args()
    main(args.file, args.prefix, args.baseline,
         resolve=args.resolve, visualize=args.visualize)
