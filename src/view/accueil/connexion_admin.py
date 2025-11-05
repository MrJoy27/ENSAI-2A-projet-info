from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.admin_service import adminService


class ConnexionAdmin(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et mot de passe
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

        # Appel du service pour trouver le joueur
        admin = adminService().se_connecter(pseudo, mdp)

        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if admin:
            message = f"Vous êtes connecté en tant qu'administrateur"
            Session().connexion(admin)

            from view.menu_admin_vue import MenuAdminVue

            return MenuAdminVue(message)

        message = "Erreur de connexion (pseudo ou mot de passe invalide)"
        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
