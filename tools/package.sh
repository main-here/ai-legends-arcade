#!/bin/sh
# Builds dist/ai-legends-arcade-itch.zip for itch.io: index.html at the zip root + assets/ (no tools, no docs)
set -e
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/ai-legends-arcade-itch.zip
zip -q -r -X dist/ai-legends-arcade-itch.zip index.html assets -x '*.DS_Store'
unzip -l dist/ai-legends-arcade-itch.zip | tail -1
ls -lh dist/ai-legends-arcade-itch.zip
