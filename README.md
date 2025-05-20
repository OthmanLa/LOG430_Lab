
1. Architecture du projet
    LOG430_Lab/
    ├── app/                  
    │   ├── __init__.py
    │   └── main.py           
    ├── tests/
    │   └── test_main.py      
    ├── Dockerfile           
    ├── docker-compose.yml    
    ├── requirements.txt     
    ├── .dockerignore         
    └── .github/workflows/ci.yml  # pipeline Lint → Tests → Build → Push
   
2. Mise en route pas à pas
   2.1 Cloner le projet
     git clone https://github.com/OthmanLa/LOG430_Lab.git
      cd LOG430_Lab
   2.2 Lancer le conteneur avec Docker Compose
     docker compose up --build -d
     docker compose logs app
      → Hello, World!
     docker compose down
   Ps: le docker-compose.yml pointe déjà vers othman157/log430_lab:latest. Un simple docker compose up -d suffit.
   docker run --rm othman157/log430_lab:latest

4. Pipeline CI/CD
   <img width="650" alt="image" src="https://github.com/user-attachments/assets/a7a09d88-9e7a-4796-b80b-6fce2f9c48c6" />

   <img width="650" alt="image" src="https://github.com/user-attachments/assets/d648a4de-3326-4e2d-9c38-840e87db22e7" />
   

   





   
