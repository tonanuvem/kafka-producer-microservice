#!/bin/sh
set -e

# Verifica se já foi configurado
if grep -q "inserir_webhook" Dockerfile 2>/dev/null then
    echo "Digite a URL que está no canal #webhook:"
    read WEBHOOK

    if [ -z "$WEBHOOK" ]; then
        echo "ERRO: URL não pode ser vazia."
        exit 1
    fi

    WEBHOOK_ESC=$(printf '%s' "$WEBHOOK" | sed 's/[&/\]/\\&/g')
    sed -i "s|inserir_webhook|$WEBHOOK_ESC|g" ./producer/Dockerfile
    sed -i "s|inserir_webhook|$WEBHOOK_ESC|g" ./docker-compose.yml
    echo "Webhook configurado com sucesso."
else
    echo "AVISO: Webhook já foi configurado anteriormente."
    echo "Para reconfigurar, execute: git checkout Dockerfile"
fi

#echo "Digite a URL que está no canal #webhook do SLACK:"
#read WEBHOOK

#sed -i 's|inserir_webhook|'$WEBHOOK'|' Dockerfile
# sed -i 's|lab-produtor|lab-testes|' Dockerfile
