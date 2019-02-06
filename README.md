# kafka-producer-microservice
Kafka Producer - Microservice

> docker run --name produtor_Kafka -p 5001:5001 --rm --net=host --env TOPICO=meu-topico --env HOST=IP --env PORTA=9092 -d tonanuvem/64aoj_producer_kafka:latest

Vamos criar variáveis de ambiente: 

> export TOPICO=meu-topico 

> export HOST=IP 

> export PORTA=9092 

> echo $TOPICO $HOST $PORTA
