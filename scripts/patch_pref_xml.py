#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET

pref_file = sys.argv[1]

NS_ANDROID = 'http://schemas.android.com/apk/res/android'
NS_SETTINGS = 'http://schemas.android.com/apk/res-auto'

ET.register_namespace('android', NS_ANDROID)
ET.register_namespace('settings', NS_SETTINGS)

tree = ET.parse(pref_file)
root = tree.getroot()

already = any(
    e.get(f'{{{NS_ANDROID}}}key') == 'keybox_data_setting'
    for e in root.iter()
)

if already:
    print("Preferences already added")
    sys.exit(0)

keybox = ET.SubElement(root,
    'com.android.settings.security.KeyboxDataPreference')
keybox.set(f'{{{NS_ANDROID}}}order', '253')
keybox.set(f'{{{NS_ANDROID}}}key', 'keybox_data_setting')
keybox.set(f'{{{NS_ANDROID}}}title', '@string/keybox_data_title')
keybox.set(f'{{{NS_ANDROID}}}summary', '@string/keybox_data_summary')
keybox.set(f'{{{NS_ANDROID}}}defaultValue', '')

pif = ET.SubElement(root,
    'com.android.settings.security.PifDataPreference')
pif.set(f'{{{NS_ANDROID}}}order', '254')
pif.set(f'{{{NS_ANDROID}}}key', 'pif_data_setting')
pif.set(f'{{{NS_ANDROID}}}title', '@string/pif_data_title')
pif.set(f'{{{NS_ANDROID}}}summary', '@string/pif_data_summary')
pif.set(f'{{{NS_ANDROID}}}defaultValue', '')

tree.write(pref_file, encoding='utf-8', xml_declaration=True)
print("more_security_privacy_settings.xml updated")
