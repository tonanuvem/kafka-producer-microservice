FROM python:3.6-alpine
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
CMD ["python", "server.py"]
