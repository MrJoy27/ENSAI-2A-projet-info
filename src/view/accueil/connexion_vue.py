from InquirerPy import inquirer
from typing import Optional

from view.vue_abstraite import VueAbstraite
from view.session import Session

import requests
import os


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et mot de passe
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()
        print(pseudo,mdp)
        # Appel du service pour trouver le joueur
        joueur = requests.get(url=os.environ["WEBSERVICE_HOST"]+"/joueur/connexion", params={"pseudo":pseudo,"mdp":mdp}).json()
        print(os.environ["WEBSERVICE_HOST"]+"/joueur/connexion",joueur)
        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if joueur==True:
            message = f"Vous êtes connecté sous le pseudo {pseudo}"
            Session().connexion(pseudo, mdp)

            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue(message)

        message = "Erreur de connexion (pseudo ou mot de passe invalide)"
        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
