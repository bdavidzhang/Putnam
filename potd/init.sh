#!/bin/bash

# Desired date format: month-day-year (e.g., 11-09-2025)
TODAY=$(date +"%m-%d-%Y")

# Name of the folder to copy
SOURCE="template"

# Destination folder
DEST="$TODAY"

# Copy the folder
cp -r "$SOURCE" "$DEST"

echo "✅ Copied '$SOURCE' to '$DEST'"
