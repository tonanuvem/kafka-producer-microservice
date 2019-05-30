FROM python:3.6-alpine

ENV TOPICO=meu-topico
ENV HOST=0.0.0.0
ENV PORTA=9092
ENV SLACK=https://hooks.slack.com/services/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
ENV CANAL=lab-produtor

ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
CMD ["python", "server.py"]
