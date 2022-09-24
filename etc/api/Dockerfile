FROM python:3.9

WORKDIR /app
EXPOSE 8000

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./src /app

CMD ["python3", "-m", "kin_blockchain", "run-server"]
