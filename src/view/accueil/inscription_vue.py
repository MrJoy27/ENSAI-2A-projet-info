import os

import regex
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PasswordValidator
from prompt_toolkit.validation import ValidationError, Validator

from view.vue_abstraite import VueAbstraite

import requests 
import os


class InscriptionVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()

        mdp = inquirer.secret(
            message="Entrez votre mot de passe : ",
            validate=PasswordValidator(
                length=5,
                message="Au moins 5 caractères",
            ),
        ).execute()

        # Appel du service pour créer le joueur
        joueur = requests.post(url=os.environ["WEBSERVICE_HOST"]+"/joueur/", params={"pseudo":pseudo,"mdp":mdp}).json()
        # Si le joueur a été créé
        if joueur==True:
            message = (
                f"Votre compte {pseudo} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur de connexion (pseudo probablement déjà utilisé)"

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
