from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

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
                "Manche en cours",
                "Lancer une partie",
            ],
        ).execute()

        match choix:
            case "Quitter la table":
                from view.menu_joueur_vue import MenuJoueurVue
                tab_id=Session().table
                resultat=requests.delete(url=os.environ["WEBSERVICE_HOST"]+"/table/"+tab_id,params={"nom":Session().compte,"mdp":Session().mdp}).json()
                Session().table=None
                return MenuJoueurVue(resultat)

            case "Joueurs à la table":
                tab_id=Session().table
                joueurs=requests.get(url=os.environ["WEBSERVICE_HOST"]+"/table/"+tab_id).json()
                return MenuTableVue(joueurs)

            case "Manche en cours":
                tab_id=Session().table
                en_cours=requests.get(url=os.environ["WEBSERVICE_HOST"]+"/manche/en_cours/"+tab_id,params={"nom":Session().compte,"mdp":Session().mdp}).json()
                if en_cours==True:
                    from view.manche_vue import MenuMancheVue
                    return MenuMancheVue()
                return MenuTableVue("Aucune manche en cours")
            case "Lancer une partie":
                tab_id=Session().table
                small=inquirer.text(message="Quelle valeur pour la small blind ?").execute()
                big=inquirer.text(message="Quelle valeur pour la big blind ?").execute()
                requests.post(url=os.environ["WEBSERVICE_HOST"]+"/manche/",params={"small":small,"big":big, "id_table":tab_id }, )
                from view.manche_vue import MenuMancheVue
                return MenuMancheVue()
