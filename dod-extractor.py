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
           'Visibility & Analytics']
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
    # (b_name, b_pages, b_columns, b_mappings),
    # (c_name, c_pages, c_columns, c_mappings),
    # (d_name, d_pages, d_columns, d_mappings),
    # (e_name, e_pages, e_columns, e_mappings),
    # (f_name, f_pages, f_columns, f_mappings),
    # (g_name, g_pages, g_columns, g_mappings),
    # (h_name, h_pages, h_columns, h_mappings),
    # (i_name, i_pages, i_columns, i_mappings),
]

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

mapping_cols = {
    91: [76],
    94: [62, 74, -1, 94, 104],
    95: [61, 74, 83, 93, -1],
    96: [62, 74, 83, 92, -1],
    103: [59, -1, -1],
    104: [60, 70, -1],
    105: [60, 70, 80],
    111: [69, 80, 90, 101],
    112: [73, -1, 95, -1],
    118: [62, 72, -1, -1],
    119: [62, 72, 82, -1],
    120: [59, 69, -1, -1],
    126: [65, 76, -1],
    127: [64, 75, -1],
    132: [78],
    135: [62, 73, 85, -1],
    141: [68, 78, -1],
    142: [66, 76, -1],
    143: [64, -1, -1],
    158: [-1, 78, 87, 97],
    159: [71, 79, 88, 98],
    160: [-1, -1, 81, -1],
    166: [80, 91],
    167: [77, -1],
    172: [52, -1, 72, 82, 92, 102, -1],
    173: [52, -1, 72, 82, 92, 102, -1],
    174: [55, -1, 76, 86, 97, 107, -1],
    175: [52, -1, 72, 82, 92, 102, -1],
    176: [-1, 59, 68, -1, -1, -1, -1],
    186: [64, 74, -1, -1],
    187: [-1, 69, -1, -1],
    190: [81],
    191: [73],
    193: [67, 77, -1],
    194: [68, 78, -1],
    195: [66, 76, -1],
    200: [66, -1, 89],
    201: [65, 76, 87],
    214: [69],
    216: [62, -1, 85, -1],
    217: [65, 76, 87, 99],
    218: [63, -1, 85, 97],
    219: [63, 74, 85, 96],
    227: [-1, -1, -1, -1],
    228: [-1, 78, -1, 99],
    229: [70, 81, 92, -1],
    230: [68, 78, -1, 100],
    231: [63, -1, -1, -1],
    237: [58, -1, -1, -1, -1, 103, -1],
    238: [59, -1, 77, -1, -1, 105, -1],
    239: [58, -1, 77, -1, 86, 104, -1],
    240: [55, -1, -1, -1, -1, 98, -1],
    249: [68, 80],
    261: [76, -1, -1],
    262: [71, -1, -1],
    266: [-1, 74, -1, 97, -1],
    267: [-1, 76, -1, 99, -1],
    272: [57, 68, 78, -1, 99, 110],
    273: [54, 63, 73, -1, 93, -1],
    277: [62, -1, 84, -1, 105],
    278: [64, -1, 86, -1, -1],
    279: [60, -1, 81, -1, -1],
    284: [66, 79, -1, -1],
    285: [69, 82, -1, -1],
    286: [-1, 76, -1, -1],
    290: [48, -1, -1, -1, -1, -1, -1],
    299: [75, 90],
    302: [-1, 73, 84, -1, 105],
    303: [-1, -1, 84, 95, 106],
    307: [78, 90],
    312: [69, 80, 90, 101],
    313: [65, -1, 85, -1],
    324: [71, 82, -1, -1],
    325: [72, 82, 93, -1],
    330: [71, -1, -1],
    332: [74],
    333: [71],
    336: [-1, 87],
    338: [74, 84, 95],
    339: [74, 85, 95],
    342: [-1, 81, -1],
    344: [61, -1, -1, -1],
    345: [61, -1, -1, 90],
    356: [-1, 85, -1],
    357: [76, 85, 95],
    361: [67, -1, 85, -1, 103],
    362: [67, 77, -1, 95, 105],
    363: [71, 81, 90, 100, -1],
    369: [75, 88],
    371: [69, -1, 90, -1],
    374: [-1, 88],
    375: [75, 89],
    377: [81, 92],
    378: [83, 94],
    379: [81, 93],
}

headings = {
    '1.1.1': 'Inventory User',
    '1.2.1': 'Implement Application Based Permissions per Enterprise',
    '1.2.2': 'Rule Based Dynamic Access Part 1',
    '1.2.3': 'Rule Based Dynamic Access Part 2',
    '1.2.4': 'Enterprise Government Roles and Permissions Part 1',
    '1.2.5': 'Enterprise Government Roles and Permissions Part 2',
    '1.8.1': 'Single Authentication',
    '4.4.3': 'File Activity Monitoring Part 2',
    '1.3.1': 'Organizational MFA/IdP',
    '1.3.2': 'Alternative Flexible MFA Part 1',
    '1.3.3': 'Alternative Flexible MFA Part 2',
    '1.4.1': 'Implement System and Migrate Privileged Users Part 1',
    '1.4.2': 'Implement System and Migrate Privileged Users Part 2',
    '1.4.3': 'Real Time Approvals and Just-in-Time (JIT)/Just-Enough-Administration (JEA)',
    '1.4.4': 'Real Time Approvals and JIT/JEA Analytics Part 2',
    '1.5.1': 'Organizational ILM',
    '1.5.2': 'Enterprise ILM Part 1',
    '1.5.3': 'Enterprise ILM Part 2',
    '1.5.4': 'Enterprise ILM Part 3',
    '1.6.1': 'Implement User',
    '1.6.2': 'User Activity Monitoring Part 1',
    '1.6.3': 'User Activity Monitoring Part 2',
    '7.3.2': 'Establish User Baseline Behavior',
    '7.2.5': 'User/Device Baselines',
    '7.4.1': 'Baseline & Profiling Part 1',
    '5.2.5': 'Real-Time Access Decisions',
    '3.4.3': 'Enrich Attributes for Resource Authorization Part 1',
    '1.7.1': 'Deny User by Default Policy',
    '1.8.2': 'Periodic Authentication',
    '1.8.3': 'Continuous Authentication Part 1',
    '1.8.4': 'Continuous Authentication Part 2',
    '3.4.1': 'Resource Authorization Part 1',
    '3.4.6': 'SDC Resource Authorization Part 1',
    '7.6.1': 'AI-enabled Network Access',
    '7.6.2': 'AI-enabled Dynamic Access Control',
    '1.9.1': 'Enterprise PKI/IdP Part 1',
    '1.9.2': 'Enterprise PKI/IdP Part 2',
    '1.9.3': 'Enterprise PKI/IdP Part 3',
    '2.1.1': 'Device Health Tool Gap Analysis',
    '2.1.2': 'NPE/PKI, Device under Management',
    '2.1.3': 'Enterprise IdP Part 1',
    '2.1.4': 'Enterprise IdP Part 2',
    '2.6.2': 'Enterprise Device Management Part 1',
    '2.4.1': 'Deny Device by Default Policy',
    '2.3.6': 'Enterprise PKI Part 1',
    '2.2.1': 'Implement C2C/Compliance Based Network Authorization Part 1',
    '4.7.4': 'Integrate Solution(s) and Policy with Enterprise IDP Part 1',
    '2.2.2': 'Implement C2C/Compliance Based Network Authorization Part 2',
    '2.4.2': 'Managed and Limited Bring Your Own Device (BYOD) &IoT Support',
    '2.5.1': 'Implement Asset, Vulnerability, and Patch Management Tools',
    '2.3.5': 'Fully Integrate Device Security stack with C2Cas Appropriate',
    '2.3.1': 'Entity Activity Monitoring Part 1',
    '2.3.2': 'Entity Activity Monitoring Part 2',
    '2.3.3': 'Implement Application Control and FIM Tools',
    '2.3.4': 'Integrate NextGen AV Tools with C2C',
    '2.3.7': 'Enterprise PKI Part 2',
    '2.7.1': 'Implement Endpoint Detection & Response Tools and Integrate with C2C',
    '2.4.4': 'Managed and Full BYOD & IOT Support Part 2',
    '2.6.1': 'Implement UEDM or equivalent Tools',
    '2.4.3': 'Managed and Full BYOD and IoT Support Part 1',
    '3.2.3': 'Automate Application Security & Code Remediation Part 1',
    '2.6.3': 'Enterprise Device Part 2',
    '2.7.2': 'Implement XDR Tools and Integrate with C2C Part 1',
    '2.7.3': 'Implement XDR Tools and Integrate with C2C Part 2',
    '7.2.1': 'Threat Alerting Part 1',
    '7.2.3': 'Threat Alerting Part 3',
    '3.1.1': 'Application/Code Identification',
    '3.2.1': 'Build DevSecOps Software Factory Part 1',
    '3.2.2': 'Build DevSecOps Software Factory Part 2',
    '3.2.4': 'Automate Application Security & Code Remediation Part 2',
    '3.5.1': 'cATO Part 1',
    '3.3.3': 'Vulnerability Management Program Part 2',
    '3.4.5': 'REST API Micro-Segments',
    '3.3.1': 'Approved Binaries/Code',
    '3.3.2': 'Vulnerability Management Program Part 1',
    '3.3.4': 'Continual Validation',
    '3.4.2': 'Resource Authorization Part 2',
    '3.4.4': 'Enrich Attributes for Resource Authorization Part 2',
    '3.4.7': 'SDC Resource Authorization Part 2',
    '5.3.1': 'Datacenter Macro-segmentation',
    '5.4.2': 'Application & Device Micro-segmentation',
    '4.3.3': 'Manual Data Tagging Part 2',
    '4.6.3': 'DLP Enforcement via Data Tags and Analytics Part 2',
    '4.5.4': 'DRM Enforcement via Data Tags and Analytics Part 2',
    '3.5.2': 'cATO Part 2',
    '6.1.1': 'Policy Inventory & Development',
    '6.7.4': 'Automated Workflow',
    '4.1.1': 'Data Analysis',
    '4.2.1': 'Define Data Tagging Standards',
    '4.2.2': 'Interoperability Standards',
    '4.2.3': 'Develop SDS Policy',
    '4.3.1': 'Implement Data Tagging & Classification Tools',
    '4.3.2': 'Manual Data Tagging Part 1',
    '6.3.1': 'Implement Data Tagging & Classification ML Tools',
    '4.5.1': 'Implement DRM and Protection Tools Part 1',
    '4.7.1': 'Integrate DAAS Access with SDS Policy Part 1',
    '4.7.6': 'Implement SDS Tool and/or integrate with DRM Tool Part 1',
    '4.3.4': 'Automated Data Tagging & Support Part 1',
    '4.3.5': 'Automated Data Tagging & Support Part 2',
    '4.6.1': 'Implement DLP Enforcement Points',
    '4.5.3': 'DRM Enforcement via Data Tags and Analytics Part 1',
    '4.6.2': 'DLP Enforcement via Data Tags and Analytics Part 1',
    '4.4.1': 'DLP Enforcement Point Logging and Analysis',
    '4.4.2': 'DRM Enforcement Point Logging and Analysis',
    '4.4.4': 'File Activity Monitoring Part 2',
    '4.4.5': 'Database Activity Monitoring',
    '4.4.6': 'Comprehensive Data Activity Monitoring',
    '4.5.2': 'Implement DRM and Protection Tools Part 2',
    '4.5.5': 'DRM Enforcement via Data Tags and Analytics Part 3',
    '4.6.4': 'DLP Enforcement via Data Tags and Analytics Part 3',
    '5.4.3': 'Process Micro-segmentation',
    '4.7.2': 'Integrate DAAS Access with SDS Policy Part 2',
    '4.7.3': 'Integrate DAAS Access with SDS Policy Part 3',
    '4.7.5': 'Integrate Solution(s) and Policy with Enterprise IdP Part 2',
    '4.7.7': 'Implement SDS Tool and/or Integrate with DRM Tool Part 2',
    '5.1.1': 'Define Granular Control Access Rules & Policies Part 1',
    '5.1.2': 'Define Granular Control Access Rules & Policies Part 2',
    '5.2.1': 'Define SDN APIs',
    '5.2.2': 'Implement SDN Programable Infrastructure',
    '5.2.3': 'Segment Flows into Control',
    '5.2.4': 'Network Asset Discovery & Optimization',
    '6.6.2': 'Standardized API Calls & Schemas Part 1',
    '5.3.2': 'Base/Camp/Post/Station (B/C/P/S) Macro-segmentation',
    '6.1.4': 'Enterprise Security Profile Part 2',
    '5.4.1': 'Implement Micro-segmentation',
    '5.4.4': 'Protect Data in Transit',
    '6.1.2': 'Organization Access Profile',
    '6.1.3': 'Enterprise Security Profile Part 1',
    '6.2.1': 'Task Automation Analysis',
    '6.2.2': 'Enterprise Integration & Workflow Provisioning Part 1',
    '6.2.3': 'Enterprise Integration & Workflow Provisioning Part 2',
    '6.4.1': 'Implement AI Automation Tools',
    '6.4.2': 'AI Driven by Analytics Decides Automation and Orchestration Modifications',
    '6.5.1': 'Response Automation Analysis',
    '6.5.2': 'Implement SOAR Tools',
    '6.5.3': 'Implement Playbooks',
    '6.7.1': 'Workflow Enrichment Part 1',
    '6.6.1': 'Tool Compliance Analysis',
    '6.6.3': 'Standardized API Calls & Schemas Part 2',
    '6.7.2': 'Workflow Enrichment Part 2',
    '6.7.3': 'Workflow Enrichment Part 3',
    '7.1.1': 'Scale Considerations',
    '7.1.2': 'Log Parsing Name',
    '7.1.3': 'Log Analysis',
    '7.2.4': 'Asset Identification (ID) & Alert Correlation',
    '7.3.1': 'Implement Analytics Tools',
    '7.2.2': 'Threat Alerting Part 2',
    '7.5.1': 'Cyber Threat Intelligence Program Part 1',
    '7.4.2': 'Baseline & Profiling Part 2',
    '7.4.3': 'UEBA Baseline Support Part 1',
    '7.4.4': 'UEBA Baseline Support Part 2',
    '7.5.2': 'Cyber Threat Intelligence Program Part 2',
}

dod_types = { 'T': 'Target',
              'A': 'Advanced' }

dod_techs = { 'S': 'System',
              'O': 'Organization',
              'O/S': 'System/Organization' }

def process_section(reader, pages, columns, mappings, find=False, types=None, techs=None, phases=None):
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
                    categories = []
                    for index in x_marks:
                        col = columns[index]
                        if col in headings:
                            heading = headings[col]
                            entry = { 'activity': f"{col} {heading}" }
                        else:
                            entry = { 'pillar': col }
                        if types is not None:
                            entry['type'] = dod_types[types[index]]
                        if techs is not None:
                            entry['tech'] = dod_techs[techs[index]]
                        if phases is not None:
                            entry['phase'] = phases[index]
                        categories.append(entry)

                    entry = {'key': m.group(1), 'categories': categories}
                    result.append(entry)
        if find:
            print(f'    {p+1}: {sorted(found)},')
    return result

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

    # print(f"Cap {cap}, tech {techs}, types {types}, phases {phases}")

    for num in range(page_num, page_num + count):
        indices = mapping_cols[num + 1]
        if len(indices) != len(types):
            print(f"Warning: column count mismatch on page {num + 1}, {indices}, {types}", file=sys.stderr)

        columns = [f"{cap}.{n}" for n in range(1, 20)]
        r = process_section(reader, [num], columns, mapping_cols, types=types, techs=techs, phases=phases)
        result.append({'name': cap,
                       'mappings': r})
    return result

def process_file_subs(reader):
    result = []
    for (page, count) in sub_pages:
        r = process_sub(reader, page, count)
        result.extend(r)
    return result

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
        result = process_file_subs(reader)
        print(yaml.dump(result))
    elif args.page:
        process_section(reader, [args.page - 1], [], {args.page: []}, find=True)
    else:
        result = process_file(reader)
        print(yaml.dump(result))
