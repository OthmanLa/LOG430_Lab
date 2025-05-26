from app.db.session import Session
from app.models.produit import Produit
from app.models.vente import Vente, LigneVente

def enregistrer_vente():
    session = Session()
    lignes = []
    total = 0.0

    try:
        while True:
            nom = input("Nom du produit (ou 'fin' pour terminer) : ")
            if nom.lower() == 'fin':
                break

            produit = session.query(Produit).filter(Produit.nom.ilike(nom)).first()
            if not produit:
                print(f"Produit '{nom}' non trouvé.")
                continue

            quantite = int(input(f"Quantité à acheter (disponible : {produit.quantite}) : "))
            if quantite <= 0:
                print("Quantité invalide.")
                continue

            if quantite > produit.quantite:
                print("Stock insuffisant.")
                continue

            sous_total = produit.prix * quantite
            total += sous_total

            ligne = LigneVente(produit_id=produit.id, quantite=quantite, sous_total=sous_total)
            lignes.append(ligne)

            produit.quantite -= quantite  

        if not lignes:
            print("Aucune ligne de vente saisie.")
            return

        vente = Vente(total=total, lignes=lignes)
        session.add(vente)
        session.commit()
        print(f"Vente enregistrée. Total : {total:.2f}$")

    except Exception as e:
        session.rollback()
        print(" Erreur lors de l'enregistrement de la vente :", e)
    finally:
        session.close()
