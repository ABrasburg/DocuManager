#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[update] git pull..."
cd "$REPO_DIR"
git pull

echo "[update] Actualizando dependencias del backend..."
cd "$REPO_DIR/back"
source .venv/bin/activate
pipenv install --deploy --ignore-pipfile 2>/dev/null || pip install -q -r <(pipenv requirements)
deactivate

echo "[update] Rebuildeando frontend..."
cd "$REPO_DIR/front"
npm install --silent
NODE_OPTIONS=--openssl-legacy-provider npm run build

chmod -R o+rX "$REPO_DIR/front/build" 2>/dev/null || true

echo "[update] Reiniciando backend..."
sudo systemctl restart documanager-backend

echo "[update] Listo."
