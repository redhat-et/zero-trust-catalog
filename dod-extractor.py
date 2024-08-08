#!/usr/bin/env python3

from argparse import ArgumentParser, BooleanOptionalAction
from pypdf import PdfReader
import re
import sys
import yaml

# Appendix A - Control Tables Allocated to Pillars

a_name= 'Appendix A - Control Tables Allocated to Pillars'
a_pages = range(43, 65)
a_columns=['Enabler', 'User', 'Device', 'Application & Workload', 'Data',
           'Network & Environment', 'Automation & Orchestration',
           'Visibility and Analytics']
a_mappings = {
    44: [89, 95, 102, 108, 114, 120, 127, 133],
    45: [-1, 97, 104, 110, 117, -1, 129, 136],
    46: [69],
    47: [85, 91, 98, 105, 111, -1, 124, 131],
    48: [77, -1, -1, 101, -1, 117],
    49: [88, -1, 100, 106, -1, 118],
    50: [83, -1, -1, -1, -1, -1, -1, 128],
    51: [75, 83, 92, 100, -1, -1, 125],
    52: [-1, 91, 100, -1, -1, -1, -1, 146],
    53: [90, -1, -1, -1, -1, -1, 128, 134],
    54: [],
    55: [84, 91],
    56: [85, 91, -1, 103, -1, -1, -1, 127],
    57: [69, 78],
    58: [83, -1, -1, -1, 109, -1, 122],
    59: [84, 91, 97, 104, 110, -1, 124, 130],
    60: [79, -1, -1, 102, -1, -1, 125],
    61: [88, 94, 101, 107, 114, 120, -1, 133],
    62: [-1, 97, 104, 111, 117, 124, 131, 137],
    63: [89, 96, 103, 110, 117, 123, 130, 137],
    64: [-1, -1, 111, 118, 125, 133, 140, 147],
    65: [82, -1, -1, 101],
}

# Appendix B - Execution Enabler Overlay

b_name = 'Appendix B - Execution Enabler Overlay'
b_pages = range(67, 69)
b_columns = ['Doctrine', 'Organization', 'Training', 'Materiel', 'Leadership and education',
           'Personnel', 'Facilities', 'Policy']
b_mappings = {
    68: [-1, 93, 100, 108, 116, 123],
    69: [-1, 87, 94],
}

# Appendix C - User Pillar Overlay

c_name = 'Appendix C - User Pillar Overlay'
c_pages = range(84, 90)
c_columns = ['1.1 User Inventory', '1.2 Conditional User Access', '1.3 Multi-Factor Authentication (MFA)',
           '1.4 Privileged Access Management (PAM)', '1.5 Identity Federation & User Credentialing',
           '1.6 Behavioral, Contextual ID, and Biometrics', '1.7 Least Privileged Access',
           '1.8 Continuous Authentication', '1.9 Integrated ICAM Platform']
c_mappings = {
    85: [65, 76, 86, 98, 108, 119, 129, -1, 151],
    86: [65, 76, 87, 98, 109, -1, 130, -1, 152],
    87: [63, 74, 85, 95, 106, 116, 127, 137, 148],
    88: [67, 78, 89, 100, 111, 122, 133, 144, 155],
    89: [-1, 78, 89, 100, 111, 122, 133, 144, 155],
    90: [-1, -1, -1, 88, -1, 108],
}

# Appendix D - Device Pillar Overlay

d_name = 'Appendix D - Device Pillar Overlay'
d_pages = range(153, 156)
d_columns = ['2.1 Device Inventory', '2.2 Device Detection and Compliance',
           '2.3 Device Authorization w/ Real Time Inspection',
           '2.4 Remote Access',
           '2.5 Partially & Fully Automated Asset, Vulnerability and Patch Mgmt',
           '2.6 UEM & MDM', '2.7 EDR & XDR']
d_mappings = {
    153: [72, 84, 95, 107, 119, 130, 131, 142],
    154: [70, 82, 94, 105, 117, 128, 140],
    155: [73, 85, 97, 109, 121, 133, 145],
    156: [73, 84, 96, 108, 120, 132, 143],
}

# Appendix E - Application & Workload Pillar Overlay

e_name = 'Appendix E - Application & Workload Pillar Overlay'
e_pages = range(208, 212)
e_columns = ['3.1 Application Inventory', '3.2 Secure Software Development & Integration',
           '3.3 Software Risk Management', '3.4 Resource Authorization & Integration',
           '3.5 Continuous Monitoring and Ongoing Authorizations']
e_mappings = {
    209: [-1, 105, 118, 130],
    210: [91, 103, 115, 128, 140],
    211: [-1, 105, 118, 130],
    212: [-1, 106, 118, 130]
}

# Appendix F - Data Pillar Overlay

f_name = 'Appendix F - Data Pillar Overlay'
f_pages = range(255,258)
f_columns = ['4.1 Data Catalog Risk Alignment', '4.2 DoD Enterprise Data Governance',
           '4.3 Data Labeling and Tagging', '4.4 Data Monitoring and Sensing',
           '4.5 Data Encryption & Rights Management', '4.6 Data Loss Prevention',
           '4.7 Data Access Control']
f_mappings = {
    256: [-1, 87, 99, 111, 123, 135, 148],
    257: [74, 87, 99, 111, 123, 135],
    258: [-1, -1, 90, 101, 112, 124]
}

# Appendix G - Network & Environment Pillar Overlay

g_name = 'Appendix G - Network & Environment Pillar Overlay'
g_pages = range(295, 297)
g_columns = ['5.1 Data Flow Mapping', '5.2 Software Defined Networking (SDN)',
           '5.3 Macro-segmentation', '5.4 Micro-segmentation']
g_mappings = {
    296: [102, 112, 123, 132],
    297: [105, 116, 126, 136],
}

# Appendix H - Automation & Orchestration Pillar Overlay

h_name = 'Appendix H - Automation & Orchestration Pillar Overlay'
h_pages = range(319,322)
h_columns = ['6.1 Policy Decision Point & Policy Orchestration', '6.2 Critical Process Automation',
           '6.3 Machine Learning', '6.4 Artificial Intelligence',
           '6.5 Security Orchestration, Automation & Response', '6.6 API Standardization',
           '6.7 Security Operations Center & Incident Response']
h_mappings = {
    320: [86, -1, 106, -1, 127],
    321: [89, 99, 110, 120, 131, -1, 152],
    322: [-1, -1, -1, -1, -1, 1, 129],
}

# Appendix I - Visibility & Analytics Pillar Overlay

i_name = 'Appendix I - Visibility & Analytics Pillar Overlay'
i_pages = range(351,355)
i_columns = ['7.1 Log All Traffic (Network, Data, Apps, Users)',
           '7.2 Security Information and Event Management (SIEM)',
           '7.3 Common Security and Risk Analytics',
           '7.4 User and Entity Behavior Analytics',
           '7.5 Threat Intelligence Integration',
           '7.6 Automated Dynamic Policies']
i_mappings = {
    352: [-1, 90, 101, 112, -1, 134],
    353: [86, 97, 109, -1, 132, 144],
    354: [87, 99, 111, 123, 135, 147],
    355: [-1, 91, -1, -1, 124, 135],
}

control_pattern = re.compile(r'^ ?(\w+-\d+(\(\d+\))?)')

rulesets = [
    (a_name, a_pages, a_columns, a_mappings),
    (b_name, b_pages, b_columns, b_mappings),
    (c_name, c_pages, c_columns, c_mappings),
    (d_name, d_pages, d_columns, d_mappings),
    (e_name, e_pages, e_columns, e_mappings),
    (f_name, f_pages, f_columns, f_mappings),
    (g_name, g_pages, g_columns, g_mappings),
    (h_name, h_pages, h_columns, h_mappings),
    (i_name, i_pages, i_columns, i_mappings),
]

def process_section(reader, pages, columns, mappings, find=False):
    result = []
    for p in pages:
        page = reader.pages[p]
        text = page.extract_text(extraction_mode="layout", layout_mode_strip_rotated=False)

        found = set()
        for line in text.splitlines():
            m = control_pattern.match(line)
            if m:
                if find:
                    x_marks = [pos for pos, char in enumerate(line) if char == 'X']
                    found = found | set(x_marks)
                else:
                    indices = mappings[p+1]
                    x_marks = [index for index, pos in enumerate(indices) if 'X' in line[pos-1:pos+1]]
                    categories = [columns[index] for index in x_marks]
                    # print(f'{m.group(1):>10}, {categories}')
                    result.append({'key': m.group(1), 'categories': categories})

        if find:
            print(f'    {p+1}: {sorted(found)},')
    return result

cap_pattern = re.compile(r'^\s*Capability:?\s+(\d\.\d)')
tech_pattern = re.compile(r'^\s*Tech.*[,)]\s+(.*)$')
type_pattern = re.compile(r'^\s*Activity \w+ \(Target,(?: Advanced\))?\s+(.*)$')
phase_pattern = re.compile(r'^\s*Phase[^)]+\)\s+(.*)$')

sub_pages = [(90, 1), (93, 3), (102, 3), (110, 2), (117, 3), (125, 2), (131, 1), (134, 1), (140, 3),
             (157, 3), (165, 2), (171, 5), (185, 2), (189, 2), (192, 3), (199, 2),
             (213, 1), (215, 4), (226, 5), (236, 4), (248, 1),
             (260, 2), (265, 2), (271, 2), (276, 3), (283, 3), (289, 1),
             (298, 1), (301, 2), (306, 1), (311, 2),
             (323, 2), (329, 1), (331, 2), (335, 1), (337, 2), (341, 1), (343, 2),
             (355, 2), (360, 3), (368, 1), (370, 1), (373, 2), (376, 3)
             ]

def process_sub(reader, page_num, count):
    result = []
    page = reader.pages[page_num]
    text = page.extract_text(extraction_mode="layout", layout_mode_strip_rotated=False)

    cap = None
    techs = None
    types = None
    phases = None

    for line in text.splitlines():
        m = cap_pattern.match(line)
        if m:
            cap = m.group(1)
        m = tech_pattern.match(line)
        if m:
            techs = m.group(1).split()
        m = type_pattern.match(line)
        if m:
            types = m.group(1).split()
        m = phase_pattern.match(line)
        if m:
            phases = m.group(1).split()

    if cap is None:
        print(f"Warning: failed to match 'Capability' on page {page_num}", file=sys.stderr)
    if techs is None:
        print(f"Warning: failed to match 'Tech/Non-Tech' on page {page_num}", file=sys.stderr)
    if types is None:
        print(f"Warning: failed to match 'Activity Type' on page {page_num}", file=sys.stderr)
    if phases is None:
        print(f"Warning: failed to match 'Phase' on page {page_num}", file=sys.stderr)

    if cap is None or techs is None or types is None or phases is None:
        print(text, file=sys.stderr)
    elif len(techs) != len(types) or len(types) != len(phases):
        print(f"Warning: captured lists with differing lengths", file=sys.stderr)

    print(f"Cap {cap}, tech {techs}, types {types}, phases {phases}")

def process_file_subs(reader):
    for (page, count) in sub_pages:
        process_sub(reader, page, count)

def process_file(reader):
    result = []

    for (name, pages, columns, mappings) in rulesets:
        r = process_section(reader, pages, columns, mappings)
        result.append({'name': name, 'mappings': r})
    return result

if __name__ == '__main__':

    parser = ArgumentParser(description='Extract DoD zero trust control mappings from PDF')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='The PDF file')
    parser.add_argument('-c', '--find-columns', dest='page', type=int,
                        help='Find table "X" columns on a page')
    parser.add_argument('-s', '--sub-sections', action=BooleanOptionalAction,
                        help='Extract sub-section pages')
    args = parser.parse_args()

    reader = PdfReader(args.file)

    if args.sub_sections:
        process_file_subs(reader)
    elif args.page:
        process_section(reader, [args.page - 1], [], {args.page: []}, find=True)
    else:
        result = process_file(reader)
        print(yaml.dump(result))
