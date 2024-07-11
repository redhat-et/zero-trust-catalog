#!/usr/bin/env python3

from argparse import ArgumentParser, BooleanOptionalAction
import json
import re
import sys
import uuid
import yaml

can_ignore = ['at', 'ca', 'cp', 'ir', 'ma', 'mp', 'pe', 'pl', 'pm', 'ps', 'pt', 'ra']

pillars = ['Enabler', 'User', 'Device', 'Application & Workload', 'Data',
           'Network & Environment', 'Automation & Orchestration',
           'Visibility and Analytics']
mappings = { p: [] for p in pillars }
controls_by_id = { }
baselines_by_name = { }
seen_ids = { }
mapped_ids = { }

profile_uuid = str(uuid.uuid4())
import_uuid = str(uuid.uuid4())

html_preamble = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>NIST Controls by DoD Pillar</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
          crossorigin="anonymous">
    <style>dt { float: left; width: 3em; } dd { margin-bottom: 0; }</style>
  </head>
  <body>
  <div class="container-fluid border-bottom" style="padding-top: 1em; padding-bottom: 1em; margin-bottom: 1em;">
  <button style="float: right;" type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#legend">
    Legend
  </button>
    <header class="d-flex justify-content-center">
      <h3>NIST SP 800-53 rev5 Controls by DoD pillar and NIST baseline</h3>
    </header>
  </div>

  <div class="modal" id="legend" aria-hidden="true">
  <div class="modal-dialog modal-xl">
  <div class="modal-content">
    <div class="modal-header">
      <h1 class="modal-title fs-5" id="exampleModalLabel">NIST Control Families</h1>
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body">
    <div class="row">
      <div class="col">
        <dl>
          <dt>ac</dt><dd>Access Control</dd>
          <dt>at</dt><dd>Awareness and Training</dd>
          <dt>au</dt><dd>Audit and Accountability</dd>
          <dt>ca</dt><dd>Assessment, Authorization and Monitoring</dd>
          <dt>cm</dt><dd>Configuration Management</dd>
          <dt>cp</dt><dd>Contingency Planning</dd>
          <dt>ia</dt><dd>Identification and Authentication</dd>
          <dt>ir</dt><dd>Incident Response</dd>
          <dt>ma</dt><dd>Maintenance</dd>
          <dt>mp</dt><dd>Media Protection</dd>
        </dl>
      </div>
      <div class="col">
        <dl>
          <dt>pe</dt><dd>Physical and Environmental Protection</dd>
          <dt>pl</dt><dd>Planning</dd>
          <dt>pm</dt><dd>Program Management</dd>
          <dt>ps</dt><dd>Personnel Security</dd>
          <dt>pt</dt><dd>Personally Identifiable Information Processing and Transparency</dd>
          <dt>ra</dt><dd>Risk Assessment</dd>
          <dt>sa</dt><dd>System and Services Acquisition</dd>
          <dt>sc</dt><dd>System and Communications Protection</dd>
          <dt>si</dt><dd>System and Information Integrity</dd>
          <dt>sr</dt><dd>Supply Chain Risk Management</dd>
        </dl>
      </div>
    </div>
    </div>
  </div>
  </div>
  </div>
'''

html_postamble = '''
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
          crossorigin="anonymous"></script>
  <script>
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
const offcanvasElementList = document.querySelectorAll('.offcanvas')
const offcanvasList = [...offcanvasElementList].map(offcanvasEl => new bootstrap.Offcanvas(offcanvasEl))
  </script>
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
        profile = json.load(file).get('profile')

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

def is_withdrawn(id):
    control = controls_by_id[id]
    props = { prop['name'] : prop for prop in control['props'] }
    return 'status' in props and props['status']['value'] == 'withdrawn'

def generate_control(id, classes, guidance=False):
    mapped_ids[id] = id
    text = controls_by_id[id]['title']
    if guidance:
        return f'<a href="#{id}" class="{classes}" data-bs-toggle="offcanvas">{id}</a>'
    else:
        return f'<span class="{classes}" data-bs-toggle="tooltip" data-bs-title="{text}">{id}</span>'


param_pattern = re.compile(r'{{ insert: param, (\S+) }}')

def resolve_text(text, params):

    def replace(m):
        id = m.group(1)
        if id not in params:
            print(f"Warning: {id} not in this control", file=sys.stderr)
            return id
        param = params[id]
        if 'label' in param:
            repl =  param['label']
        elif 'select' in param:
            repl = " | ".join(param['select']['choice'])
        else:
            repl = id

        return f'<span style="background-color: yellow;">< {repl} ></span>'

    return param_pattern.sub(replace, text)

part_names = {
    'statement' : 'Statement',
    'guidance' : 'Guidance',
    'assessment-objective': 'Assessment Objective',
    'assessment-method' : 'Assessment Method',
}

linebreak_pattern = re.compile(r'\n\n', flags=re.M)
href_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

def md_to_link(m):
    label = m.group(1)
    href = m.group(2)
    return f'<a href="{href}" data-bs-toggle="offcanvas">{label}</a>'

def resolve_parts(parts, params, top=False):
    html = []

    for part in parts:
        if top and part['name'] in part_names:
            title = part_names[part['name']]
            html.append(f'<h5 style="padding-top: 0.5em;">{title}</h5>')
        if 'props' in part:
            props = { p['name'] : p['value'] for p in part['props'] }
            if 'label' in props:
                label = props['label']
                html.append(f'<b class="label">{label}</b>')
        if 'prose' in part:
            text = resolve_text(part['prose'], params)
            text = linebreak_pattern.sub('<br/>', text)
            text = href_pattern.sub(md_to_link, text)

            html.append(f'<span class="text">{text}</span><br/>')
        if 'parts' in part:
            html.append('<div class="container-fluid">')
            html.extend(resolve_parts(part['parts'], params))
            html.append('</div>')

    return html

def resolve_control(id):
    control = controls_by_id[id]
    if 'params' not in control:
        params = []
    else:
        params = { param['id'] : param for param in control['params'] }

    html = resolve_parts(control['parts'], params, top=True)
    return html

def generate_html(guidance=False):
    html = []

    html.append('<div class="container-fluid">')
    html.append('<div class="row align-items-end">')
    html.append('<div class="col"></div>')
    for p in pillars:
        html.append('<div class="col">')
        html.append(f'<h5>{p}</h5>')
        html.append('</div>')
    html.append('</div>')

    # controls in NIST baselines AND DoD pillars

    for i, k in reversed(list(enumerate(baselines_by_name.keys()))):
        style = styles[i]
        head = headings[i]
        classes = f'badge bg-{style}-subtle text-{style}'

        baseline_ids = { id : id for id in baselines_by_name[k] }

        html.append('<div class="row align-items-end">')
        html.append('<div class="col">')
        html.append(f'<h5>{head} Baseline</h5>')
        html.append('</div>')

        for p in pillars:
            html.append('<div class="col">')

            for id in mappings[p]:
                if id in baseline_ids:
                    html.append(generate_control(id, classes, guidance))

            html.append('</div>')
        html.append('</div>')

    # controls only in DoD pillars

    html.append('<div class="row align-items-end">')
    html.append('<div class="col">')
    html.append(f'<h5>No baseline</h5>')
    html.append('</div>')
    style = 'secondary'
    classes = f'badge bg-{style}-subtle text-{style}'
    for p in pillars:
        html.append('<div class="col">')
        for id in mappings[p]:
            if id not in mapped_ids:
                html.append(generate_control(id, classes, guidance))
        html.append('</div>')
    html.append('</div>')

    html.append('</div>') # container-fluid

    # controls only in NIST baselines

    html.append('<div class="container-fluid" style="padding-top: 2em; padding-bottom: 1em;">')
    html.append('<h5>Controls in NIST baselines that are not mapped to DoD pillars</h5>')
    for i, k in reversed(list(enumerate(baselines_by_name.keys()))):
        style = styles[i]
        classes = f'badge bg-{style}-subtle text-{style}'
        for id in baselines_by_name[k]:
            if id not in mapped_ids:
                html.append(generate_control(id, classes, guidance))
    html.append('</div>')

    # NIST controls not referenced by DoD or by NIST baselines

    html.append('<div class="container-fluid" style="padding-bottom: 1em;">')
    html.append('<h5>Controls not in any DoD pillars or NIST baselines</h5>')
    style = 'secondary'
    classes = f'badge bg-{style}-subtle text-{style}'
    for id in controls_by_id.keys():
        if id not in mapped_ids:
            if id[:2] in can_ignore:
                continue
            if is_withdrawn(id):
                continue
            html.append(generate_control(id, classes, guidance))
    html.append('</div>')

    # Ignored NIST controls not referenced elsewhere

    html.append('<div class="container-fluid" style="padding-bottom: 1em;">')
    html.append('<h5>Ignored controls not referenced elsewhere</h5>')
    style = 'secondary'
    classes = f'badge bg-{style}-subtle text-{style}'
    for id in controls_by_id.keys():
        if id not in mapped_ids:
            if is_withdrawn(id):
                continue
            html.append(generate_control(id, classes, guidance))
    html.append('</div>')

    # Guidance text popup div blocks

    if guidance:
        html.append('<div class="container">')
        for id in controls_by_id.keys():
            if is_withdrawn(id):
                continue
            control = controls_by_id[id]
            title = control['title']
            html.append(f'<div class="offcanvas offcanvas-bottom" id="{id}">')
            html.append('<div class="offcanvas-header">')
            html.append(f'<h4>{id.upper()} – {title}</h4>')
            html.append('<button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>')
            html.append('</div>')
            html.append('<div class="offcanvas-body">')
            html.extend(resolve_control(id))
            html.append('</div>')
            html.append('</div>')
        html.append('</div>')

    return "\n".join(html)

def main(filename, prefix, baselines, resolve=False, visualize=False, guidance=False):

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
        print(generate_html(guidance))
        print(html_postamble)
    else:
        for p in pillars:
            controls = mappings[p]
            write_profile(p, prefix, controls, resolve)

if __name__ == '__main__':

    parser = ArgumentParser(description='Generate OSCAL profiles for each DoD pillar')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='The DoD annotated NIST controls in JSON')
    parser.add_argument('-p', '--prefix', type=str, default='dod-profile',
                        help='Filename prefix for generated profiles')
    parser.add_argument('-r', '--resolve', action=BooleanOptionalAction,
                        help='Include control definitions inline, not just as imports')
    parser.add_argument('-b', '--baseline', type=str, action='append',
                        help='Include NIST baseline information')
    parser.add_argument('-V', '--visualize', action=BooleanOptionalAction,
                        help='Generate a visualization of controls by pillar')
    parser.add_argument('-g', '--guidance', action=BooleanOptionalAction,
                        help='Include guidance notes from the specifcation')
    args = parser.parse_args()
    main(args.file, args.prefix, args.baseline,
         resolve=args.resolve, visualize=args.visualize, guidance=args.guidance)
