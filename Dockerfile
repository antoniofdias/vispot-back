FROM python:3.9-slim-buster

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 1337

CMD ["python3.9", "server.py"]
