FROM python:2.7

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000


