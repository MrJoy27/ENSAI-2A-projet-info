from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import compteService
from service.admin_service import adminService


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

        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

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
                for i in range(len(Session().table.liste_comptes)):
                    if Session().table.liste_comptes[i] == Session().compte:
                        Session().table.liste_comptes.pop(i)
                Session().table = None
                Session().table_vide()
                return MenuJoueurVue()

            case "Joueurs à la table":
                lc = []
                for compte in Session().table.liste_comptes:
                    lc.append([compte.nom, compte.nb_jetons])
                return MenuTableVue(lc)

            case "Lancer une partie":
                tab = Session().table
                if len(tab.liste_comptes) < 2:
                    return MenuTableVue("Pas assez de joueurs pour lancer une partie")
