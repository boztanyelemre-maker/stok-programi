# Render (Docker runtime) — Python Web Service
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=naron.settings

# Statik dosyalar (veritabanı gerekmez)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Render PORT ortam değişkenini kullanır; migrate çalışma anında (DATABASE_URL ile)
CMD sh -c "python manage.py migrate --noinput && exec gunicorn naron.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --timeout 120"
