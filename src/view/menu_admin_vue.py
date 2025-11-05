from InquirerPy import inquirer

from utils.reset_database import ResetDatabase

from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.menu_joueur_vue import MenuJoueurVue

from service.joueur_service import compteService
from service.admin_service import adminService


class MenuAdminVue(VueAbstraite):
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
                "Afficher les joueurs de la base de données",
                "Créditer un compte",
                "Infos de session",
                "Supprimer un compte",
                "Réinitialiser la base de données",
                "Se déconnecter"
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Infos de session":
                return MenuAdminVue(Session().afficher())

            case "Afficher les joueurs de la base de données":
                joueurs_str = adminService().afficher_tous()
                return MenuAdminVue(joueurs_str)

            case "Créditer un compte":
                nom = inquirer.text(message="Nom du compte à créditer : ").execute()
                nbj = int(inquirer.text(message="Nombre de jetons à créditer : ").execute())
                if not isinstance(nbj, int):
                    raise TypeError("Le nombre de jetons doit être un entier")
                else:
                    adminService().crediter(nom, nbj)
                return MenuAdminVue("Compte crédité")

            case "Supprimer un compte":
                nom = inquirer.text(message="Nom du compte à supprimer : ").execute()
                success = adminService().supprimer(nom)
                vali = inquirer.confirm("Êtes-vous sûr ?").execute()
                if not vali:
                    return MenuAdminVue()
                if success:
                    return MenuAdminVue(f"Compte {nom} supprimé")
                else:
                    return MenuAdminVue()
            
            case "Réinitialiser la base de données":
                vali = inquirer.confirm("Êtes-vous sûr ?").execute()
                if vali:
                    succes = ResetDatabase().lancer()
                    message = (
                        f"Ré-initilisation de la base de données - {'SUCCES' if succes else 'ECHEC'}"
                    )
                return MenuAdminVue()
