FROM python:3.6-alpine

ENV TOPICO=meu-topico
ENV HOST=0.0.0.0
ENV PORTA=9092
ENV SLACK=inserir-webhook
ENV CANAL=lab-produtor
#ENV CANAL=lab-testes

ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
EXPOSE 5001
CMD ["python", "server.py"]
