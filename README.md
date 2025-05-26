
1. Architecture du projet
    LOG430_Lab/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── controllers/
│ ├── db/
│ └── models/
├── tests/
│ └── test_main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
└── .github/workflows/ci.yml # Lint → Tests → Build → Push (Docker Hub)
   
2. Mise en route pas à pas
   2.1 Cloner le projet
     git clone https://github.com/OthmanLa/LOG430_Lab.git
      cd LOG430_Lab
   2.2 Lancer le conteneur avec Docker Compose
        docker-compose build
        docker-compose run --rm app
    Cela démarre l'application en console :
        Ajouter un produit
        Rechercher un produit
        Enregistrer une vente

Voir le stock
     docker compose down
   Ps: le docker-compose.yml pointe déjà vers othman157/log430_lab:latest. Un simple docker compose up -d suffit.
   docker run --rm othman157/log430_lab:latest

4. Pipeline CI/CD
   
   <img width="650" alt="image" src="https://github.com/user-attachments/assets/d648a4de-3326-4e2d-9c38-840e87db22e7" />
   <img width="647" alt="image" src="https://github.com/user-attachments/assets/69dd34fd-ea16-4ca3-badd-10fcdc351110" />

   

   





   
