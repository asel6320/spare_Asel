FROM python:3.12.7-slim-bookworm
ENV PYTHONBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt
COPY source/ /app
EXPOSE 8000
