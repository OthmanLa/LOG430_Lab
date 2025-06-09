# import threading
# import time
# from app.db.session import Session
# from app.models.vente import Vente, LigneVente
# from app.models.produit import Produit
# from datetime import datetime
# import random

# def vente_auto(caisse_id):
#     session = Session()
#     try:
#         produits = session.query(Produit).all()
#         if not produits:
#             print(f"Aucun produit caisse: {caisse_id}")
#             return

#         produit = random.choice(produits)
#         quantite = min(1, produit.quantite)

#         if quantite <= 0:
#             print(f"Stock vide pour {produit.nom} (caisse {caisse_id})")
#             return

#         ligne = LigneVente(produit_id=produit.id, quantite=quantite, sous_total=quantite * produit.prix)
#         vente = Vente(date=datetime.now(), total=ligne.sous_total, caisse_id=caisse_id, lignes=[ligne])

#         produit.quantite -= quantite

#         session.add(vente)
#         session.commit()

#         print(f"Vente enregistrée dans la caisse {caisse_id} - {quantite}x {produit.nom} - total {vente.total:.2f}$")

#     except Exception as e:
#         session.rollback()
#         print(f"Erreur caisse {caisse_id} : {e}")
#     finally:
#         session.close()

# if __name__ == "__main__":
#     threads = []
#     for i in range(1, 4):
#         t = threading.Thread(target=vente_auto, args=(i,))
#         threads.append(t)
#         t.start()
#         time.sleep(0.1)

#     for t in threads:
#         t.join()

#     print("Toutes les ventes parallèles sont terminées.")
