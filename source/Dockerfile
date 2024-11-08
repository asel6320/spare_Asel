FROM python:3.12-alpine
ENV PYTHONBUFFERED=1
RUN apk add --no-cache bash
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt
COPY . .
EXPOSE 8000

