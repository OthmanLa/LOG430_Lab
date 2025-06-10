# Image de base Python légère
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
