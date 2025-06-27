#!/bin/bash
echo "📦 Initialisation de la base..."
python app/init_db.py

echo "🚀 Lancement de FastAPI sur le port 8010..."
exec uvicorn main:app --host 0.0.0.0 --port 8010
