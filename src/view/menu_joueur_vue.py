from InquirerPy import inquirer
from typing import Optional

from business_object.compte import Compte
from business_object.joueur import Joueur
from business_object.table import Table

from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.table_vue import MenuTableVue

import requests
import os

class MenuJoueurVue(VueAbstraite):
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
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Rejoindre une table",
                "Créer une table",
                "Infos de session",
                "Supprimer son compte",
                "Se déconnecter"
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Infos de session":
                return MenuJoueurVue(Session().afficher())
            
            case "Supprimer son compte":
                from view.accueil.accueil_vue import AccueilVue

                pseudo = Session().compte
                mdp = inquirer.secret(message="Mot de passe : ").execute()
                check = inquirer.confirm("Êtes-vou sûr ?").execute()
                if check:
                    supression=requests.delete(os.environ["WEBSERVICE_HOST"]+"/joueur"+pseudo, params={"mdp" :mdp})
                    if supression==True:
                        return AccueilVue("Compte supprimé")
                    else:
                        return MenuJoueurVue("Une erreur est survenue, probablement un mauvais mot de passe")
                else:
                    return MenuJoueurVue

            case "Rejoindre une table":
                pseudo=Session().compte
                mdp=Session().mdp
                id_table=inquirer.text(message="Quel table voulez-vous rejoindre ?").execute()
                table_rejointe=requests.put(url=os.environ["WEBSERVICE_HOST"]+"/table/"+id_table,params={"nom": pseudo,"mdp":mdp}).json()
                if table_rejointe==True: 
                    Session().table=id_table
                    return MenuTableVue(f"Table {id_table} rejointe")
                else:
                    return MenuJoueurVue("Une erreur est survenue. Table non rejointe")
            
            case "Créer une table":
                id=requests.post(url=os.environ["WEBSERVICE_HOST"]+"/table/").json()
                return MenuJoueurVue(f"Table {id} créee")




