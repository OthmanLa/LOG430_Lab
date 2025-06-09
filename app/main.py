from app.db.init_db import init_db
from app.controllers.produit_controller import ajouter_produit, rechercher_produit
from app.controllers.vente_controller import enregistrer_vente, afficher_ventes_par_caisse
from app.controllers.stock_controller import afficher_stock_magasin

def afficher_menu_caisse():
    print("\n--- Système de caisse ---")
    print("1. Ajouter un produit")
    print("2. Rechercher un produit")
    print("3. Enregistrer une vente")
    print("4. Voir les ventes de cette caisse")
    print("5. Changer de caisse")
    print("6. Voir le stock du magasin")
    print("7. Consulter le stock central")
    print("8. Demander un réapprovisionnement")
    print("9. Quitter")

def menu_caisse(caisse_id, magasin_id):
    while True:
        afficher_menu_caisse()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            nom = input("Nom du produit : ")
            prix = float(input("Prix : "))
            ajouter_produit(nom, prix)

            from app.controllers.stock_controller import ajouter_stock
            from app.db.session import SessionLocal
            from app.models.produit import Produit

            quantite = int(input("Quantité à ajouter dans le magasin actuel : "))
            session = SessionLocal()
            produit = session.query(Produit).filter_by(nom=nom).first()
            session.close()

            if produit:
                ajouter_stock(magasin_id, produit.id, quantite)

        elif choix == "2":
            nom = input("Nom à rechercher : ")
            rechercher_produit(nom)

        elif choix == "3":
            enregistrer_vente(caisse_id, magasin_id)

        elif choix == "4":
            afficher_ventes_par_caisse(caisse_id=caisse_id, magasin_id=magasin_id)

        elif choix == "5":
            print("Changement de caisse demandé.")
            return

        elif choix == "6":
            afficher_stock_magasin(magasin_id)

        elif choix == "7":
            from app.controllers.stock_controller import consulter_stock_central
            consulter_stock_central()

        elif choix == "8":
            from app.controllers.stock_controller import demander_reapprovisionnement
            produit_id = int(input("ID du produit à réapprovisionner : "))
            quantite = int(input("Quantité à demander : "))
            demander_reapprovisionnement(magasin_id, produit_id, quantite)

        elif choix == "9":
            print("Merci, à bientôt !")
            return False

        else:
            print("Choix invalide.")

def menu_maison_mere():
    while True:
        print("\n--- Menu Maison Mère ---")
        print("1. Générer un rapport consolidé")
        print("2. Voir le tableau de bord")
        print("3. Modifier un produit")
        print("4. Ajouter un nouveau produit au Centre Logistique")
        print("5. Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            from app.controllers.rapport_controller import generer_rapport_consolide
            generer_rapport_consolide()

        elif choix == "2":
            from app.controllers.dashboard_controller import afficher_tableau_de_bord
            afficher_tableau_de_bord()
        
        elif choix == "3":
            from app.controllers.produit_controller import modifier_produit
            modifier_produit()
        
        elif choix == "4":
            from app.controllers.produit_controller import ajouter_produit_centre
            ajouter_produit_centre()

        elif choix == "5":
            print("Déconnexion de la maison mère.")
            return False

        else:
            print("Choix invalide.")

def menu():
    init_db()

    while True:
        try:
            caisse_id = int(input("Sur quelle caisse souhaitez-vous travailler ? (1 à 3) ou 0 pour Maison Mère : "))
            if caisse_id == 0:
                if menu_maison_mere() == False:
                    break
            elif caisse_id in [1, 2, 3]:
                magasin_id = int(input("Dans quel magasin êtes-vous ? (1 à 5) : "))
                if magasin_id in [1, 2, 3, 4, 5]:
                    if menu_caisse(caisse_id, magasin_id) == False:
                        break
                else:
                    print("Magasin invalide.")
            else:
                print("Choix invalide.")
        except ValueError:
            print("Entrée invalide.")



if __name__ == "__main__":
    print("Bienvenue dans le système de caisse.")
    menu()



def hello() -> str:
    """Return the greeting message"""
    return "Hello, World!"

if __name__ == "__main__":
    #Display the message
    print(hello())