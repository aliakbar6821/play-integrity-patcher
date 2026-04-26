#!/bin/bash
set -e

SETTINGS_OUT="$1"
HELPER_SMALI="$2"

echo "=== Patching Settings APK ==="

SMALI_DIR="$SETTINGS_OUT/smali"
for d in "$SETTINGS_OUT"/smali_classes*; do
    [ -d "$d" ] && SMALI_DIR="$d"
done
echo "Using smali dir: $SMALI_DIR"

echo "Copying preference classes..."
mkdir -p "$SMALI_DIR/com/android/settings/security"

for f in "$HELPER_SMALI/com/android/settings/security/PifDataPreference"*.smali; do
    [ -f "$f" ] && cp "$f" "$SMALI_DIR/com/android/settings/security/" && \
        echo "Copied: $(basename $f)"
done

for f in "$HELPER_SMALI/com/android/settings/security/KeyboxDataPreference"*.smali; do
    [ -f "$f" ] && cp "$f" "$SMALI_DIR/com/android/settings/security/" && \
        echo "Copied: $(basename $f)"
done

echo "Adding resources..."
mkdir -p "$SETTINGS_OUT/res/layout"
mkdir -p "$SETTINGS_OUT/res/drawable"
cp resources/layout/pref_with_delete.xml "$SETTINGS_OUT/res/layout/"
cp resources/drawable/ic_trash_can.xml "$SETTINGS_OUT/res/drawable/"

echo "Adding strings..."
python3 scripts/patch_strings.py "$SETTINGS_OUT/res/values/strings.xml"

echo "Patching preference XML..."
python3 scripts/patch_pref_xml.py \
    "$SETTINGS_OUT/res/xml/more_security_privacy_settings.xml"

echo "Patching MoreSecurityPrivacyFragment..."
FRAGMENT=$(find "$SMALI_DIR" \
    -name "MoreSecurityPrivacyFragment.smali" | head -1)

if [ -z "$FRAGMENT" ]; then
    echo "ERROR: MoreSecurityPrivacyFragment.smali not found"
    find "$SMALI_DIR" -name "*MoreSecurity*" 2>/dev/null
    exit 1
fi

python3 scripts/patch_fragment.py "$FRAGMENT"

echo "=== Settings APK patching complete ==="
