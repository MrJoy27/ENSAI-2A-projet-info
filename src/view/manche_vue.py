from InquirerPy import inquirer
from typing import Optional

from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.table_vue import MenuTableVue

import requests
import os

class MenuMancheVue(VueAbstraite):
    """Vue du menu du joueur

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
        print("\n" + "-" * 50 + "\nMenu Manche\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Etat de la manche",
                "Suivre",
                "Se coucher",
                "Relancer",
                "Quitter menu manche",
            ],
        ).execute()

        match choix:
            case "Etat de la manche":
                tab_id=Session().table
                etat=requests.get(os.environ["WEBSERVICE_HOST"]+"/manche/"+tab_id, params={"nom": Session().compte, "mdp": Session().mdp}).json()
                return MenuMancheVue(etat) 
            case "Suivre":
                tab_id=Session().table
                etat=requests.put(os.environ["WEBSERVICE_HOST"]+"/manche/"+tab_id, params={"nom": Session().compte, "mdp": Session().mdp, "choix": "Suivre"}).json()
                if etat is not None:
                    return MenuMancheVue(etat)
                else:
                    return MenuMancheVue()
            case "Se coucher":
                tab_id=Session().table
                etat=requests.put(os.environ["WEBSERVICE_HOST"]+"/manche/"+tab_id, params={"nom": Session().compte, "mdp": Session().mdp, "choix": "Se coucher"}).json()
                if etat is not None:
                    return MenuMancheVue(etat)
                else:
                    return MenuMancheVue()
            case "Relancer":
                tab_id=Session().table
                relance=inquirer.text(message="De combien souhaitez-vous relancer ?").execute()
                etat=requests.put(os.environ["WEBSERVICE_HOST"]+"/manche/"+tab_id, params={"nom": Session().compte, "mdp": Session().mdp, "choix": "Relancer", "nb_jetons":relance}).json()
                if etat is not None:
                    return MenuMancheVue(etat)
                else:
                    return MenuMancheVue()
            case "Quitter menu manche":
                from view.table_vue import MenuTableVue
                return MenuTableVue()