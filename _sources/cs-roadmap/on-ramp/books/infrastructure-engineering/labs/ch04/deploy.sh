#!/usr/bin/env bash
# Deploy one built artifact (a version) to the staging folder.
set -euo pipefail
VERSION="$1"

rm -rf staging && mkdir staging
tar -xzf "artifacts/greet-$VERSION.tar.gz" -C staging
echo "$VERSION" > staging/VERSION
echo "staging now runs version $VERSION"
