FROM python3.9

WORKDIR /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./src /app

CMD ['python', '-m', 'kin_blockchain', 'run_server']
