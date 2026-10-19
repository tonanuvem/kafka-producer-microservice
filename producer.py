from kafka import KafkaProducer
from flask import make_response, abort
import requests
import json, os

_producer = None


def get_producer():
    """Cria (uma única vez) e reutiliza a conexão com o Kafka."""
    global _producer
    if _producer is None:
        broker = os.environ['HOST'] + ":" + os.environ['PORTA']
        print(broker)
        # --------
        # USAGE: https://kafka-python.readthedocs.io/en/master/usage.html
        _producer = KafkaProducer(bootstrap_servers=[broker], value_serializer=lambda m: json.dumps(m, ensure_ascii=False).encode('utf-8'))
    return _producer


def create(msg):
    try:
        texto = msg.get("texto", None)
        topico = msg.get("topico") or os.environ.get("TOPICO")
        producer = get_producer()

        # Asynchronous by default
        future = producer.send(topico, msg)
        # Block for 'synchronous' sends
        record_metadata = future.get(timeout=10)

    except Exception as e:
        # Decide what to do if produce request failed...
        print(repr(e))
        abort(
            406,
            "Erro ao enviar msg pro Kafka: "+repr(e),
        )

    # Successful result returns assigned partition and offset
    print ('Sucesso no envio. Topico: '+str(record_metadata.topic)+' Particao :' + str(record_metadata.partition) + ' Offset: ' + str(record_metadata.offset))
    postMSG_criada(texto)
    return make_response(
        "Evento criado: "+str(texto), 201
    )

def postMSG_criada(msg):
    # format payload for slack
    # para o Microsoft Teams, usa somente o campo Text (https://docs.microsoft.com/pt-br/outlook/actionable-messages/message-card-reference#card-examples)
    sdata = formatMSG(msg)
    url = os.environ['WEBHOOK']
    if url == "inserir_webhook":
        return
    # Continua com o envio somente se a URL do Webhook estiver configurada:
    r = requests.post(url, sdata, headers={'Content-Type': 'application/json'})
    if 200 <= r.status_code < 300:
      print('SUCCEDED: Sent webhook (HTTP %s)' % r.status_code)
    else:
      print('FAILED: Send webhook (HTTP %s)' % r.status_code)

def formatMSG(msg):
  url = os.environ['WEBHOOK']
  if 'hooks.slack.com' in url:
    canal = os.environ['CANAL']
    payload = {
      "channel": canal,
      "username": 'app_kafka_producer',
      "text": msg,
      "icon_emoji": ':mailbox_with_mail:'
    }
  else:
    payload = {
      "@type": "MessageCard",
      "@context": "http://schema.org/extensions",
      "themeColor": "0072C6",
      "summary": "Nova Mensagem",
      "sections": [{
        "activityTitle": msg,
        "activitySubtitle": "Solicitado via Kafka Producer",
        "activityImage": "https://cdn-icons-png.magnific.com/512/2648/2648618.png"
        #"activityImage": "https://cdn4.iconfinder.com/data/icons/pop-scenes/1000/workspace___work_from_home_laptop_computer_drink_beverage-1024.png"
      }]
    }
  return json.dumps(payload)
