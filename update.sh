#!/bin/bash

REPO="https://github.com/think1st/jarvis.git"
TARGET_DIR="$HOME/jarvis-assistant"

cd "$TARGET_DIR"

echo "📡 Checking for updates..."

git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "🚀 New update available! Updating now..."
  git pull origin main
  source venv/bin/activate
  pip install -r requirements.txt --upgrade
  echo "✅ Jarvis updated."
else
  echo "✅ You’re already up to date."
fi
