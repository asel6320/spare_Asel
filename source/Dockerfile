FROM python:3.12.7-slim-bookworm
ENV PYTHONBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY source/ /app
RUN python manage.py compilemessages
EXPOSE 8000
CMD ["gunicorn", "detail_shop.wsgi:application", "--bind", "0.0.0.0:8000"]
