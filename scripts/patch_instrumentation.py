#!/usr/bin/env python3
import sys
import re

instr_file = sys.argv[1]

with open(instr_file, 'r') as f:
    content = f.read()

if 'PropImitationHooks' in content:
    print("Already patched")
    sys.exit(0)

attach_pattern = (
    r'(invoke-virtual \{[^}]+\}, '
    r'Landroid/app/Application;'
    r'->attach\(Landroid/content/Context;\)V)'
)

replacement = (
    r'\1\n\n'
    r'    invoke-static {p2}, '
    r'Lcom/android/internal/util/PropImitationHooks;'
    r'->setProps(Landroid/content/Context;)V'
)

new_content = re.sub(attach_pattern, replacement, content)

if new_content == content:
    print("WARNING: Pattern not found, trying fallback...")
    lines = content.split('\n')
    new_lines = []
    in_new_app = False
    patched = False
    for line in lines:
        new_lines.append(line)
        if 'method public newApplication' in line:
            in_new_app = True
        if in_new_app and '->attach(' in line and not patched:
            new_lines.append('')
            new_lines.append(
                '    invoke-static {p2}, '
                'Lcom/android/internal/util/PropImitationHooks;'
                '->setProps(Landroid/content/Context;)V'
            )
            patched = True
        if in_new_app and line.strip() == 'return-object v0':
            in_new_app = False
    new_content = '\n'.join(new_lines)

with open(instr_file, 'w') as f:
    f.write(new_content)

print("Instrumentation.smali patched successfully")
