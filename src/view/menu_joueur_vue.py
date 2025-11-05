from InquirerPy import inquirer
from typing import Optional

from business_object.compte import Compte
from business_object.joueur import Joueur
from business_object.table import Table
from business_object.table import liste_tables

from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.table_vue import MenuTableVue

from service.joueur_service import compteService
from service.admin_service import adminService


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

                nom = Session().compte.nom
                mdp = inquirer.secret(message="Mot de passe : ").execute()
                check = inquirer.confirm("Êtes-vou sûr ?").execute()
                if check:
                    compte = Compte(nom=nom, mdp=mdp)
                    compteService().supprimer(compte)
                
                return AccueilVue("Compte supprimé")

            case "Rejoindre une table":
                compte = Session().compte
                table = inquirer.select(
                    message="Choisir une table à rejoindre",
                    choices=[tab for tab in liste_tables if len(table.liste_comptes) < 10]
                    )
                table.liste_comptes.append(compte)
                Session().rejoindre_table(table)
                return MenuTableVue(f"Table {table.id} rejointe")
            
            case "Créer une table":
                compte = Session().compte
                table = Table(len(liste_tables)+1)
                table.liste_comptes.append(compte)
                Session().rejoindre_table(table)
                return MenuTableVue(f"Table {table.id} créée")




