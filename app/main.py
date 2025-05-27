from app.db.init_db import init_db
from app.controllers.produit_controller import ajouter_produit, rechercher_produit
from app.controllers.vente_controller import enregistrer_vente
caisse_id = None

def afficher_menu():
    print("\n--- Système de caisse ---")
    print("1. Ajouter un produit")
    print("2. Rechercher un produit")
    print("3. Enregistrer une vente")
    print("4. Voir les ventes de cette caisse")
    print("5. Changer de caisse")
    print("6. Quitter")


def menu(caisse_id):
    init_db()

    while True:
        if caisse_id is None:
            try:
                caisse_id = int(input("Sur quelle caisse souhaitez-vous travailler ? (1, 2 ou 3) : "))
                if caisse_id not in [1, 2, 3]:
                    print("Choix invalide")
                    caisse_id = None
                    continue
            except ValueError:
                print("Erreur")
                continue

        afficher_menu()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            nom = input("Nom du produit : ")
            prix = float(input("Prix : "))
            quantite = int(input("Quantité : "))
            ajouter_produit(nom, prix, quantite)

        elif choix == "2":
            nom = input("Nom à rechercher : ")
            rechercher_produit(nom)

        elif choix == "3":
            enregistrer_vente(caisse_id)

        elif choix == "4":
            nom = input("Afficher l'historique de vente de cette caisse")
            from app.controllers.vente_controller import afficher_ventes_par_caisse
            afficher_ventes_par_caisse(caisse_id)

        elif choix == "5":
            nom = input("Changer de caisse")
            caisse_id = None
            print("Changement de caisse demandé.")

        elif choix == "6":
            print("Merci, à bientôt !")
            break

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    print("Bienvenue dans le système de caisse.")
    while True:
        try:
            caisse_id = int(input("Choisir une caisse ? (1, 2 ou 3) : "))
            if caisse_id in [1, 2, 3]:
                break
            else:
                print("Veuillez entrer 1, 2 ou 3.")
        except ValueError:
            print("Entrée invalide.")
    menu(caisse_id)
