#!/usr/bin/env python3
import sys

secure_file = sys.argv[1]

with open(secure_file, 'r') as f:
    content = f.read()

if 'pif_data' in content:
    print("Already patched, skipping")
    sys.exit(0)

new_constants = """
# PIF_DATA constant - added by patcher
.field public static final PIF_DATA:Ljava/lang/String; = "pif_data"

# FETCHED_PIF constant - added by patcher
.field public static final FETCHED_PIF:Ljava/lang/String; = "fetched_pif"

# KEYBOX_DATA constant - added by patcher
.field public static final KEYBOX_DATA:Ljava/lang/String; = "keybox_data"

"""

first_field = content.find('.field public static final')
if first_field == -1:
    print("ERROR: Could not find field declarations")
    sys.exit(1)

content = content[:first_field] + new_constants + content[first_field:]

with open(secure_file, 'w') as f:
    f.write(content)

print("Settings$Secure.smali patched successfully")
