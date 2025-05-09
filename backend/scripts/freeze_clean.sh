#!/bin/bash

# Absolute target path (Linux-style for Git Bash / WSL)
TARGET_DIR="/c/Users/Ibukunoluwa/Documents/00_Lock_In/Dev/Projects/ColorPaletteExtractor/backend"

echo "📦 Freezing dependencies (excluding pywin32)..."
pip freeze | grep -viE 'pywin32|pypiwin32|wmi|win32com' > "$TARGET_DIR/requirements.txt"

echo "✅ Clean requirements.txt written to: $TARGET_DIR/requirements.txt"
