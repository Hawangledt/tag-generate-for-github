FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /app

WORKDIR /app




