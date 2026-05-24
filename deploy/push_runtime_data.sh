#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/moomoo-backend/app}"
DATA_DIR="${DATA_DIR:-/opt/moomoo-backend/data}"

cd "${APP_DIR}"
git config --global --add safe.directory "${APP_DIR}" 2>/dev/null || true

mkdir -p data

for name in asset_snapshots.json trade_deals.json; do
  if [[ -f "${DATA_DIR}/${name}" ]]; then
    cp "${DATA_DIR}/${name}" "data/${name}"
  fi
done

git add data/asset_snapshots.json data/trade_deals.json

if git diff --cached --quiet; then
  echo "No runtime data changes to push."
  exit 0
fi

git commit -m "Update runtime data $(date -u +%Y-%m-%d)"
git push
