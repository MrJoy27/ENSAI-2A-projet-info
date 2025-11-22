from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import compteService
from service.admin_service import adminService

import requests
import os

class MenuTableVue(VueAbstraite):
    """Vue du menu d'une table

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisie par l'utilisateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu Table\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Quitter la table",
                "Joueurs à la table",
                "Lancer une partie",
            ],
        ).execute()

        match choix:
            case "Quitter la table":
                from view.menu_joueur_vue import MenuJoueurVue
                tab_id=Session().table
                resultat=requests.delete(url=os.environ["WEBSERVICE_HOST"]+"/table/"+tab_id,params={"nom":Session().compte,"mdp":Session().mdp}).json()
                return MenuJoueurVue(resultat)

            case "Joueurs à la table":
                tab_id=Session().table
                joueurs=requests.get(url=os.environ["WEBSERVICE_HOST"]+"/table/"+tab_id).json()
                return MenuTableVue(joueurs)

            case "Lancer une partie":
                tab = Session().table
                if len(tab.liste_comptes) < 2:
                    return MenuTableVue("Pas assez de joueurs pour lancer une partie")
