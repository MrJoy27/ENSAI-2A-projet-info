from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.compte import Compte
from dao.compte_dao import compteDao
from dao.admin_dao import adminDao


class compteService:
    """Classe contenant les méthodes de service des comptes"""

    @log
    def creer(self, nom, mdp) -> Compte:
        """Création d'un compte à partir de ses attributs"""
        return Compte(nom, mdp) if compteDao().creer(nom, mdp) else None

    @log
    def modifier(self, compte) -> Compte:
        """Modification d'un compte"""

        compte.mdp = hash_password(compte.mdp, compte.nom)
        return compte if compteDao().modifier(compte) else None

    @log
    def supprimer(self, compte) -> bool:
        """Supprimer le compte d'un compte"""
        return compteDao().supprimer(compte)

    @log
    def se_connecter(self, nom, mdp) -> Compte:
        """Se connecter à partir de nom et mdp"""
        return compteDao().se_connecter(nom, mdp)
