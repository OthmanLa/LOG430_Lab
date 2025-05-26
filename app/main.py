"""
Small hello-world module for LOG430 lab.

This module exposes a single function `hello` and prints the greeting when
executed as a script.
"""

def hello() -> str:
    """Return the greeting message."""
    return "Hello, World!"


from app.db.init_db import init_db
from app.controllers.produit_controller import ajouter_produit, rechercher_produit
from app.controllers.vente_controller import enregistrer_vente


def afficher_menu():
    print("\n--- Système de caisse ---")
    print("1. Ajouter un produit")
    print("2. Rechercher un produit")
    print("3. Enregistrer une vente")
    print("4. Quitter")

def menu():
    init_db()
    while True:
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
            enregistrer_vente()

        elif choix == "4":
            print("Merci, à bientôt !")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    # Display Hello World
    print(hello())

    # Lancer le menu
    menu()
