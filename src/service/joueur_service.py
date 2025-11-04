from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.compte import Compte
from dao.compte_dao import compteDao
from dao.admin_dao import adminDao


class compteService:
    """Classe contenant les méthodes de service des comptes"""

    @log
    def creer(self, nom, mdp, age, mail, fan_pokemon) -> Compte:
        """Création d'un compte à partir de ses attributs"""

        nouveau_compte = Compte(
            nom=nom,
            mdp=hash_password(mdp, nom),
            age=age,
            mail=mail,
            fan_pokemon=fan_pokemon,
        )

        return nouveau_compte if compteDao().creer(nouveau_compte) else None

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
    def se_connecter(self, nom, mdp) -> compte:
        """Se connecter à partir de nom et mdp"""
        return compteDao().se_connecter(nom, hash_password(mdp, nom))
