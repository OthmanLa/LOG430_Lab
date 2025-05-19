# Image de base Python légère
FROM python:3.11-slim

# Pas de .pyc et stdout non bufferisé
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code source
COPY . .

CMD ["python", "app/main.py"]
