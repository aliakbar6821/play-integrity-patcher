#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET

strings_file = sys.argv[1]

new_strings = [
    ('keybox_data_title', 'Select keybox XML to spoof'),
    ('keybox_data_summary',
     'Select the keybox XML used for system-wide key attestation spoofing. '
     'Click delete to reset keybox data.'),
    ('pif_data_title', 'Select PIF JSON to spoof'),
    ('pif_data_summary',
     'Select the PIF JSON for GMS/Play Store spoofing. '
     'Click delete to reset props and revert to default dynamic PIF.'),
]

ET.register_namespace('', '')
tree = ET.parse(strings_file)
root = tree.getroot()

existing = [e.get('name') for e in root.findall('string')]

for name, value in new_strings:
    if name not in existing:
        elem = ET.SubElement(root, 'string')
        elem.set('name', name)
        elem.text = value
        print(f"Added: {name}")
    else:
        print(f"Exists: {name}")

tree.write(strings_file, encoding='utf-8', xml_declaration=True)
print("strings.xml updated")
