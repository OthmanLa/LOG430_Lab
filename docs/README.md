Mise en route pas à pas 1. Cloner le projet git clone https://github.com/OthmanLa/LOG430_Lab.git cd LOG430_Lab 2. Lancer le conteneur avec Docker Compose docker-compose build docker-compose run --rm app Cela démarre l'application en console : Ajouter un produit Rechercher un produit Enregistrer une vente

Technologie	et Justification
Python--->Langage principal simple et populaire
SQLite--->Base de données légère, idéale pour un projet local
SQLAlchemy--->ORM pratique pour manipuler la DB avec Python
Docker--->Portabilité et déploiement cohérent
GitHub Actions--->Automatisation du pipeline (lint, test, build, push)
