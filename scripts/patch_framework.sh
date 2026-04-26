#!/bin/bash
set -e

FRAMEWORK_SMALI="$1"
HELPER_SMALI="$2"

echo "=== Patching framework smali ==="

echo "Copying PropImitationHooks..."
mkdir -p "$FRAMEWORK_SMALI/com/android/internal/util"
cp "$HELPER_SMALI/com/android/internal/util/PropImitationHooks.smali" \
    "$FRAMEWORK_SMALI/com/android/internal/util/" 2>/dev/null || \
    echo "WARNING: PropImitationHooks.smali not found in helper"

echo "Copying clover classes..."
mkdir -p "$FRAMEWORK_SMALI/com/android/internal/util/clover"
cp -r "$HELPER_SMALI/com/android/internal/util/clover/." \
    "$FRAMEWORK_SMALI/com/android/internal/util/clover/" 2>/dev/null || \
    echo "WARNING: clover classes not found in helper"

SECURE_FILE=$(find "$FRAMEWORK_SMALI/android/provider" \
    -name "Settings\$Secure.smali" | head -1)

if [ -z "$SECURE_FILE" ]; then
    echo "ERROR: Settings\$Secure.smali not found"
    find "$FRAMEWORK_SMALI/android/provider" -name "*.smali" 2>/dev/null | head -10
    exit 1
fi

echo "Found: $SECURE_FILE"

if grep -q "pif_data" "$SECURE_FILE"; then
    echo "Settings\$Secure.smali already has pif_data, skipping"
else
    python3 scripts/patch_settings_secure.py "$SECURE_FILE"
fi

INSTR_FILE=$(find "$FRAMEWORK_SMALI/android/app" \
    -name "Instrumentation.smali" | head -1)

if [ -z "$INSTR_FILE" ]; then
    echo "ERROR: Instrumentation.smali not found"
    exit 1
fi

echo "Found: $INSTR_FILE"

if grep -q "PropImitationHooks" "$INSTR_FILE"; then
    echo "Instrumentation.smali already patched, skipping"
else
    python3 scripts/patch_instrumentation.py "$INSTR_FILE"
fi

echo "=== Framework patching complete ==="
