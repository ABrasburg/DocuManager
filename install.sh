#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_USER="$USER"

echo "=== DocuManager - Instalación Ubuntu ==="

# --- Dependencias del sistema ---
echo "[1/6] Instalando dependencias del sistema..."
sudo apt-get update -q
sudo apt-get install -y python3 python3-pip python3-venv nginx nodejs npm

# ngrok
if ! command -v ngrok &>/dev/null; then
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt-get update -q && sudo apt-get install -y ngrok
fi

# --- Backend ---
echo "[2/6] Configurando backend..."
cd "$REPO_DIR/back"
python3 -m venv .venv
source .venv/bin/activate
pip install -q pipenv
pipenv install --deploy --ignore-pipfile 2>/dev/null || pip install -q -r <(pipenv requirements)
deactivate

# --- Frontend ---
echo "[3/6] Buildeando frontend..."
cd "$REPO_DIR/front"
npm install --silent
NODE_OPTIONS=--openssl-legacy-provider npm run build

# --- Nginx ---
echo "[4/6] Configurando nginx..."
sed "s|/REPO_DIR|$REPO_DIR|g" "$REPO_DIR/nginx.conf" | sudo tee /etc/nginx/sites-available/documanager > /dev/null
sudo ln -sf /etc/nginx/sites-available/documanager /etc/nginx/sites-enabled/documanager
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

# --- Servicios systemd ---
echo "[5/6] Instalando servicios systemd..."

sudo tee /etc/systemd/system/documanager-backend.service > /dev/null <<EOF
[Unit]
Description=DocuManager Backend (FastAPI)
After=network.target

[Service]
User=$SERVICE_USER
WorkingDirectory=$REPO_DIR/back
Environment=ENVIRONMENT=production
Environment=PORT=9000
ExecStart=$REPO_DIR/back/.venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/documanager-ngrok.service > /dev/null <<EOF
[Unit]
Description=DocuManager ngrok Tunnel
After=network.target documanager-backend.service

[Service]
User=$SERVICE_USER
ExecStart=/usr/local/bin/ngrok start --all --config /home/$SERVICE_USER/.config/ngrok/ngrok.yml
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable documanager-backend documanager-ngrok
sudo systemctl restart documanager-backend documanager-ngrok

echo "[6/6] Configurando webhook secret..."
if [ ! -f "$REPO_DIR/.webhook_secret" ]; then
    python3 -c "import secrets; print(secrets.token_hex(32))" > "$REPO_DIR/.webhook_secret"
    chmod 600 "$REPO_DIR/.webhook_secret"
    echo "  Webhook secret generado en .webhook_secret"
    echo "  Usá este valor en GitHub > Settings > Webhooks > Secret:"
    cat "$REPO_DIR/.webhook_secret"
fi

echo ""
echo "=== Instalación completa ==="
echo "Próximos pasos:"
echo "  1. Autenticá ngrok: ngrok config add-authtoken TU_TOKEN"
echo "  2. Configurá el dominio en ~/.config/ngrok/ngrok.yml"
echo "  3. Agregá el webhook en GitHub apuntando a: https://TU_DOMINIO/webhook"
echo "  4. Para ver logs: journalctl -u documanager-backend -f"
