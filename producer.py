from kafka import KafkaProducer
from kafka.errors import KafkaError
from flask import make_response, abort
from datetime import datetime
import requests
import json, os

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def create(msg):
    try:
        texto = msg.get("texto", None)
        topico = os.environ['TOPICO']
        broker = os.environ['HOST'] + ":" + os.environ['PORTA'] #"192.168.10.133:9092"
        print(broker)

        # --------
        # USAGE: https://kafka-python.readthedocs.io/en/master/usage.html
        producer = KafkaProducer(bootstrap_servers=[broker])

        # Asynchronous by default
        future = producer.send(topico, texto.encode('utf-8'))
        # Block for 'synchronous' sends
        record_metadata = future.get(timeout=10)
        
    except Exception as e:
        # Decide what to do if produce request failed...
        print(repr(e))
        abort(
            406,
            "Erro ao enviara msg pro Kafka: "+repr(e),
        )

    # Successful result returns assigned partition and offset
    print ('Sucesso no envio. Topico: '+str(record_metadata.topic)+' Particao :' + str(record_metadata.partition) + ' Offset: ' + str(record_metadata.offset))
    postMSG_criada_para_o_slack(texto)
    return make_response(
        "Mensagem criada: "+str(texto), 201
    )
    
def postMSG_criada_para_o_slack(msg):
    # format payload for slack
    sdata = formatForSlack(msg)
    url = os.environ['SLACK']
    r = requests.post(url, sdata, headers={'Content-Type': 'application/json'})
    if r.status_code == 200:
      print('SUCCEDED: Sent slack webhook')
    else:
      print('FAILED: Send slack webhook')

def formatForSlack(msg):
  canal = os.environ['CANAL']
  payload = {
    "channel":canal,
    "username":'app_kafka_producer',
    "text": msg,
    "icon_emoji":':mailbox_with_mail:'
  }
  return json.dumps(payload)
