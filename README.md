
1. Architecture du projet
LOG430_Lab/
├── microservice/
│   ├── client-service/
│   ├── commande-service/
│   ├── panier-service/
│   ├── stock-service/
│   ├── vente-service/
│   ├── produits-service/
│     ├── app/
       ├── routes/
       ├── controllers/
       ├── db/
       ├── model/ 
│    ├── Dockerfile/       
│    ├── main.py/                
│    └── requirements.txt/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api_lab3/
    │   ├── routes/
    │   ├── __init__.py      
│   ├── controllers/       
│   ├── db/                
│   └── models/          
├── tests/
│   ├── test_main.py
│   └── test_api.py        
├── Dockerfile
├── docker-compose.yml
...
├── requirements.txt
└── .github/
    └── workflows/
        └── ci.yaml
   
Mise en route pas à pas
    1. Cloner le projet
    Ouvrir un terminal et exécuter :
    git clone https://github.com/OthmanLa/LOG430_Lab.git
    cd LOG430_Lab
    2. Lancer l’environnement complet
    Le fichier docker-compose.yml orchestre tous les microservices et les outils d’infrastructure (Kong, Prometheus, Grafana). Pour tout démarrer :
    docker compose up -d
    
    
    Accès aux microservices
    Chaque microservice expose une interface Swagger UI accessible localement :
    Microservice	Adresse Swagger UI
    produits-service-1	http://localhost:8016/docs
    
    produits-service-2	http://localhost:8017/docs
    
    stock-service	http://localhost:8011/docs
    
    client-service	http://localhost:8012/docs
    
    commande-service	http://localhost:8013/docs
    
    panier-service	http://localhost:8014/docs
    
    vente-service	http://localhost:8015/docs
    
    
    Accès via Kong Gateway
    Tous les services sont également exposés via Kong Gateway à l’adresse http://localhost:8000, avec les routes suivantes :
    •	Produits : http://localhost:8000/api/v1/products
    •	Stock : http://localhost:8000/api/v1/stocks
    •	Clients, commandes, panier, ventes… disponibles sous /api/v1/...
    
    Observabilité
    •	Prometheus : http://localhost:9090
    •	Grafana : http://localhost:3000
    Identifiants par défaut : admin / admin
    Les métriques de chaque microservice sont disponibles via /metrics et agrégées dans Prometheus, visualisées dans Grafana.
    
    Arrêt et nettoyage
    Pour arrêter tous les conteneurs :
    docker compose down
    
    Lancer manuellement une image
    Pour lancer un conteneur manuellement :
    docker run --rm othman157/log430_lab:latest


   

   





   
