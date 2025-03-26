#!/bin/bash

set -e

DESKTOP_FILE="setup.desktop"
AUTOSTART_DIR="$HOME/.config/autostart"

mkdir -p "$AUTOSTART_DIR"
cp "$DESKTOP_FILE" "$AUTOSTART_DIR/"
chmod +x "$AUTOSTART_DIR/$DESKTOP_FILE"

echo "✅ Desktop launcher installed to $AUTOSTART_DIR/$DESKTOP_FILE"
echo "It will start Jarvis when the desktop environment loads."
