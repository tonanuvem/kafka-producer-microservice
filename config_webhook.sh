echo "Digite a URL que está no canal #webhook do SLACK:"
read WEBHOOK

sed -i 's|inserir_webhook|'$WEBHOOK'|' Dockerfile
# sed -i 's|lab-produtor|lab-testes|' Dockerfile


export WEBHOOK_ARG=$WEBHOOK
