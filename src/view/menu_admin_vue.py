from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

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
                "Se déconnecter",
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
                id = inquirer.text(message="Id du compte à créditer : ").execute()
                nbj = int(inquirer.text(message="Nombre de jetons à créditer : ").execute())
                if not isinstance(nbj, int):
                    raise TypeError("Le nombre de jetons doit être un entier")
                else:
                    adminService().crediter(id, nbj)
                return MenuAdminVue("Compte crédité")
