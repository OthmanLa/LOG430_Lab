from prometheus_client import Counter, start_http_server

# Nombre de notifications envoyées
notifications_envoyees = Counter("notifications_envoyees_total", "Total des notifications envoyées")

# Nombre d'événements consommés
evenements_consommes = Counter("evenements_consomme_total", "Total des événements consommés")

# Démarre un serveur HTTP pour Prometheus (port 9001)
def demarrer_serveur_prometheus():
    start_http_server(9001)  # Expose /metrics sur localhost:9001
