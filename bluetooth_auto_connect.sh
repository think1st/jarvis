#!/bin/bash

echo "🔄 Auto-connecting to trusted Bluetooth devices..."

bluetoothctl devices | while read -r _ MAC _; do
  echo "🔍 Checking $MAC..."
  bluetoothctl connect "$MAC"
done

# Wait a bit for connection to stabilize
sleep 3

# Set the default sink to the most recent Bluetooth device if available
SINK=$(pactl list short sinks | grep bluez_sink | awk '{print $2}' | head -n 1)
if [ -n "$SINK" ]; then
  echo "🎧 Setting default sink to $SINK"
  pactl set-default-sink "$SINK"
else
  echo "⚠️ No active Bluetooth sink found."
fi
