from kafka import KafkaProducer
from kafka.errors import KafkaError
from flask import make_response, abort
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def create(msg):
   
    texto = msg.get("texto", None)
    topico = "meu-topico"
    broker = "192.168.10.133:9092"
    
    # --------
    # USAGE: https://kafka-python.readthedocs.io/en/master/usage.html
    producer = KafkaProducer(bootstrap_servers=[broker])

    # Asynchronous by default
    future = producer.send(topico, texto.encode('utf-8'))
    #future = producer.send(topico, str.encode(texto))

    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        log.exception()
        abort(
            406,
            "Erro 1 ao enviara msg pro Kafka: "+str(e),
        )

    # Successful result returns assigned partition and offset
    print ('Sucesso no envio. Topico: '+str(record_metadata.topic)+' Particao :' + str(record_metadata.partition) + ' Offset: ' + str(record_metadata.offset))
    return make_response(
        "Mensagem criada: "+str(texto), 201
    )
    
    '''
    # produce keyed messages to enable hashed partitioning
    producer.send(topico, key=b'foo', value=b'bar')

    # encode objects via msgpack
    #producer = KafkaProducer(value_serializer=msgpack.dumps)
    #producer.send(topico, {'key': 'value'})
    
    # produce json messages
    producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
    producer.send(topico, {'key': 'value'})

    # produce asynchronously
    for _ in range(100):
        producer.send(topico, b'msg')

    # produce asynchronously with callbacks
    bytestr = texto.encode('utf-8')
    producer.send(topico, bytestr).add_callback(on_send_success).add_errback(on_send_error)
    
    # block until all async messages are sent
    producer.flush()

    # configure multiple retries
    producer = KafkaProducer(retries=5)

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print('I am an errback: '+str(excp))
    log.error('I am an errback', exc_info=excp)
    # handle exception
'''
