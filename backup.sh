#!/bin/bash

BACKUP_DIR="backup"
DATE=$(date +"%Y%m%d_%H%M%S")
FILENAME="jarvis_backup_$DATE.zip"

mkdir -p "$BACKUP_DIR"

zip -r "$BACKUP_DIR/$FILENAME" config/ personalities/ static/logo.png 2>/dev/null

echo "✅ Backup complete: $BACKUP_DIR/$FILENAME"
