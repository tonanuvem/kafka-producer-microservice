from kafka import KafkaProducer
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
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                    value_serializer=lambda v: str(v).encode('utf-8'))

        # Call the producer.send method with a producer-record
        producer.send('meu-topico',texto)
        return make_response(
            "Mensagem criada: ".str(texto), 201
        )

    # Otherwise, they exist, that's an error
    except Exception as e:
        abort(
            406,
            "Erro ao enviara msg pro Kafka: "+str(e),
        )

