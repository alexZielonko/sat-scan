FROM python:alpine

WORKDIR /sat-scan

COPY requirements.txt .
COPY credentials.ini .
COPY route-config.ini .

# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev curl

# Setup Python virtual environment & install deps
RUN python3 -m venv .docker_venv
RUN source .docker_venv/bin/activate
RUN pip3 install -r requirements.txt

COPY src/ .

EXPOSE 5000

CMD ["python3", "-u", "run.py"]