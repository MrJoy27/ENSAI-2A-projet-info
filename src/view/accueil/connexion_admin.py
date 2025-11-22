from InquirerPy import inquirer
from typing import Optional

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.admin_service import adminService

import requests
import os
class ConnexionAdmin(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et mot de passe
        mdp = inquirer.secret(message="Entrez le mot de passe :").execute()
        # Appel du service pour trouver le joueur
        admin = requests.get(url=os.environ["WEBSERVICE_HOST"]+"/admin/connexion", params={"mdp":mdp}).json()
        print(admin)
        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if admin==True:
            message = f"Vous êtes connecté en tant qu'administrateur"
            Session().connexion("admin",mdp)

            from view.menu_admin_vue import MenuAdminVue

            return MenuAdminVue(message)

        message = "Erreur de connexion (mot de passe invalide)"
        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
