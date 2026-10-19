#!/bin/sh
set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DOCKERFILE="$SCRIPT_DIR/Dockerfile"

# Verifica se já foi configurado
if grep -q "inserir_webhook" "$DOCKERFILE" 2>/dev/null; then
    printf "Digite a URL do webhook (Teams ou Slack): "
    read WEBHOOK

    if [ -z "$WEBHOOK" ]; then
        echo "ERRO: URL não pode ser vazia."
        exit 1
    fi

    WEBHOOK_ESC=$(printf '%s' "$WEBHOOK" | sed 's/[&|\\]/\\&/g')
    sed -i "s|inserir_webhook|$WEBHOOK_ESC|g" "$DOCKERFILE"
    echo "Webhook configurado com sucesso em $DOCKERFILE."
    echo "Reconstrua a imagem com: docker build -t producer:latest \"$SCRIPT_DIR\""
else
    echo "AVISO: Webhook já foi configurado anteriormente."
    echo "Para reconfigurar, execute: git -C \"$SCRIPT_DIR\" checkout Dockerfile"
fi
