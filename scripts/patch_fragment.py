#!/usr/bin/env python3
import sys
import re

fragment_file = sys.argv[1]

with open(fragment_file, 'r') as f:
    content = f.read()

if 'keybox_data_setting' in content:
    print("Fragment already patched")
    sys.exit(0)

print(f"Patching: {fragment_file}")

fields = '''
.field private static final KEYBOX_DATA_KEY:Ljava/lang/String; = "keybox_data_setting"
.field private static final PIF_DATA_KEY:Ljava/lang/String; = "pif_data_setting"
.field private mKeyboxFilePickerLauncher:Landroidx/activity/result/ActivityResultLauncher;
.field private mPifFilePickerLauncher:Landroidx/activity/result/ActivityResultLauncher;
.field private mKeyboxDataPreference:Lcom/android/settings/security/KeyboxDataPreference;
.field private mPifDataPreference:Lcom/android/settings/security/PifDataPreference;

'''

class_end = content.find('\n', content.find('.class ')) + 1
content = content[:class_end] + fields + content[class_end:]

oncreate_code = '''
    const-string v0, "keybox_data_setting"
    const-string v1, "pif_data_setting"

    iput-object v0, p0, Lcom/android/settings/safetycenter/MoreSecurityPrivacyFragment;->KEYBOX_DATA_KEY:Ljava/lang/String;
    iput-object v1, p0, Lcom/android/settings/safetycenter/MoreSecurityPrivacyFragment;->PIF_DATA_KEY:Ljava/lang/String;

'''

oncreate_pattern = (
    r'(\.method public onCreate\(Landroid/os/Bundle;\)V'
    r'.*?invoke-super)'
)

new_content = re.sub(
    oncreate_pattern,
    lambda m: m.group(0) + oncreate_code,
    content,
    flags=re.DOTALL
)

if new_content != content:
    content = new_content
    print("onCreate patched")
else:
    print("WARNING: Could not patch onCreate")

onview_code = '''
    const-string v0, "keybox_data_setting"
    invoke-virtual {p0, v0}, Lcom/android/settings/safetycenter/MoreSecurityPrivacyFragment;->findPreference(Ljava/lang/CharSequence;)Landroidx/preference/Preference;
    move-result-object v0
    check-cast v0, Lcom/android/settings/security/KeyboxDataPreference;
    iput-object v0, p0, Lcom/android/settings/safetycenter/MoreSecurityPrivacyFragment;->mKeyboxDataPreference:Lcom/android/settings/security/KeyboxDataPreference;
    if-eqz v0, :skip_keybox
    iget-object v1, p0, Lcom/android/settings/safetycenter/MoreSecurityPrivacyFragment;->mKeyboxFilePickerLauncher:Landroidx/activity/result/ActivityResultLauncher;
    invoke-virtual {v0, v1}, Lcom/android/settings/security/KeyboxDataPreference;->setFilePickerLauncher(Landroidx/activity/result/ActivityResultLauncher;)V
    :skip_keybox

    const-string v0, "pif_data_setting"
    invoke-virtual {p0, v0}, Lcom/android/settings/safetycenter/MoreSecurityPrivacyFragment;->findPreference(Ljava/lang/CharSequence;)Landroidx/preference/Preference;
    move-result-object v0
    check-cast v0, Lcom/android/settings/security/PifDataPreference;
    iput-object v0, p0, Lcom/android/settings/safetycenter/MoreSecurityPrivacyFragment;->mPifDataPreference:Lcom/android/settings/security/PifDataPreference;
    if-eqz v0, :skip_pif
    iget-object v1, p0, Lcom/android/settings/safetycenter/MoreSecurityPrivacyFragment;->mPifFilePickerLauncher:Landroidx/activity/result/ActivityResultLauncher;
    invoke-virtual {v0, v1}, Lcom/android/settings/security/PifDataPreference;->setFilePickerLauncher(Landroidx/activity/result/ActivityResultLauncher;)V
    :skip_pif

'''

onview_pattern = (
    r'(\.method public onViewCreated'
    r'\(Landroid/view/View;Landroid/os/Bundle;\)V'
    r'.*?invoke-super)'
)

new_content = re.sub(
    onview_pattern,
    lambda m: m.group(0) + onview_code,
    content,
    flags=re.DOTALL
)

if new_content != content:
    content = new_content
    print("onViewCreated patched")
else:
    print("WARNING: Could not patch onViewCreated")

with open(fragment_file, 'w') as f:
    f.write(content)

print("Fragment patching complete")
