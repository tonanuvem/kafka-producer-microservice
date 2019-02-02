from kafka import KafkaProducer
from kafka.errors import KafkaError
from flask import make_response, abort
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def create(msg):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    texto = msg.get("texto", None)

    # Tentando enviar a msg pro Kafka?
    try:
        # Create an instance of the Kafka producer
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        # Asynchronous by default
        future = producer.send('meu-topico', texto)

        # Block for 'synchronous' sends
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError as e:
            # Decide what to do if produce request failed...
            log.exception()
            abort(
                406,
                "Erro ao enviara msg pro Kafka: "+repr(e),
            )
            #pass
        
        # Call the producer.send method with a producer-record
        # producer.send('meu-topico',texto)
        
        return make_response(
            "Mensagem criada: "+str(texto), 201
        )

    # Otherwise, they exist, that's an error
    except Exception as e:
        abort(
            406,
            "Erro ao enviara msg pro Kafka: "+repr(e),
        )

