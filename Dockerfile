FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Code source
COPY . .

# Fichiers statiques
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Migrations + démarrage (sh -c force l'expansion de $PORT)
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn tahiti_business.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120"]
