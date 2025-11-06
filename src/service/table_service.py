from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.compte import Compte
from dao.compte_dao import compteDao
from dao.admin_dao import adminDao


class tableService:
    """Classe contenant les méthodes de service des comptes"""

    @log
    def creer(self, id):
        """Création d'une table"""
        return Table(id)

    @log
    def rejoindre(self, table, compte):
        """Rejoindre une table"""
        compte.rejoindre_table(table)

    @log
    def quitter(self, table, compte) -> bool:
        """Quitter une table"""
        compte.quitter_table(table)

    @log
    def commencer(self, table):
        """Commencer une manche"""
        return table.commencer_manche()
