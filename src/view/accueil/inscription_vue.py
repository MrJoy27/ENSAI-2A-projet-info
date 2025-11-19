import os

import regex
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PasswordValidator
from prompt_toolkit.validation import ValidationError, Validator

from service.joueur_service import compteService
from service.admin_service import adminService
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
        joueur = requests.get(url=os.environ["WEBSERVICE_HOST"]+"/joueur", params=mdp).json()

        # Si le joueur a été créé
        if joueur:
            message = (
                f"Votre compte {joueur.nom} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur de connexion (pseudo ou mot de passe invalide)"

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
