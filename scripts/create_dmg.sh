#!/bin/bash

set -e

# Use env variable passed from Python
APP_NAME="${APP_NAME:-MyApp}"
APP_BUNDLE="${APP_NAME}.app"
DMG_NAME="${APP_NAME} Installer"
DMG_FILE="${DMG_NAME}.dmg"
STAGING_DIR="dmg-staging"

echo "🚀 Creating DMG for ${APP_NAME}..."

if [ ! -d "${APP_BUNDLE}" ]; then
    echo "❌ ${APP_BUNDLE} not found!"
    exit 1
fi

rm -rf "${STAGING_DIR}" "${DMG_FILE}"
mkdir -p "${STAGING_DIR}"

cp -R "${APP_BUNDLE}" "${STAGING_DIR}/"
ln -s /Applications "${STAGING_DIR}/Applications"

hdiutil create -volname "${DMG_NAME}" -srcfolder "${STAGING_DIR}" -ov -format UDZO "${DMG_FILE}"
rm -rf "${STAGING_DIR}"

echo "✅ Created: ${DMG_FILE}"
