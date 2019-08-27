FROM python:3.6-alpine

ENV TOPICO=meu-topico
ENV HOST=0.0.0.0
ENV PORTA=9092
ENV SLACK=https://hooks.slack.com/services/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
ENV CANAL=lab-produtor

ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
EXPOSE 5001
CMD ["python", "server.py"]
