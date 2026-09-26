#!/usr/bin/env bash
# A tiny pipeline: test, build, deploy. Any failure stops the line.
set -euo pipefail
VERSION="$1"

echo "== Stage 1: test"
python3 -m unittest -q

echo "== Stage 2: build"
mkdir -p artifacts
tar -czf "artifacts/greet-$VERSION.tar.gz" greet.py
echo "built artifacts/greet-$VERSION.tar.gz"

echo "== Stage 3: deploy to staging"
./deploy.sh "$VERSION"
