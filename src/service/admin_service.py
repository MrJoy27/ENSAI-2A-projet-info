from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password
from business_object.compte import Compte
from business_object.admin import Admin
from dao.admin_dao import adminDao


class adminService:
    """Classe contenant les méthodes de service des admins"""

    @log
    def lister_tous(self, inclure_mdp=False) -> list[Compte]:
        """Lister tous les admins
        Si inclure_mdp=True, les mots de passe seront inclus
        Par défaut, tous les mdp des admins sont à None
        """
        comptes = adminDao().lister_tous()
        if not inclure_mdp:
            for j in comptes:
                j.mdp = None
        return comptes

    @log
    def trouver_par_id(self, id_compte) -> Compte:
        """Trouver un compte à partir de son id"""
        return adminDao().trouver_par_id(id_compte)

    @log
    def crediter(self, id, nb_jetons):
        """Crédit d'un compte"""
        return adminDao().crediter(id, nb_jetons)

    @log
    def supprimer(self, id) -> bool:
        """Supprimer un compte à partir de son id"""
        return adminDao().supprimer(id)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les comptes
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["nom", "nb_jetons", "nb_victoires", "nb_parties"]

        comptes = adminDao().lister_tous()

        comptes_as_list = [j.as_list() for j in comptes]

        str_comptes = "-" * 100
        str_comptes += "\nListe des comptes \n"
        str_comptes += "-" * 100
        str_comptes += "\n"
        str_comptes += tabulate(
            tabular_data=comptes_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_comptes += "\n"

        return str_comptes

    @log
    def se_connecter(self, nom, mdp) -> Admin:
        """Se connecter à partir de nom et mdp"""
        return adminDao().se_connecter(nom, mdp)

    @log
    def pseudo_deja_utilise(self, nom) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        joueurs = adminDao().lister_tous()
        return nom in [j.nom for j in joueurs]