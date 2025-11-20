from datetime import datetime
from typing import Optional

from utils.singleton import Singleton


class Session(metaclass=Singleton):
    """Stocke les données liées à une session.
    Cela permet par exemple de connaitre le joueur connecté à tout moment
    depuis n'importe quelle classe.
    Sans cela, il faudrait transmettre ce joueur entre les différentes vues.
    """

    def __init__(self):
        """Création de la session"""
        self.compte = None
        self.table = None
        self.debut_connexion = None
        self.mdp=None

    def connexion(self, compte, mdp):
        """Enregistement des données en session"""
        self.compte = compte
        self.mdp=mdp
        self.debut_connexion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def deconnexion(self):
        """Suppression des données de la session"""
        self.compte = None
        self.debut_connexion = None
        self.table = None

    def rejoindre_table(self, table):
        self.table = table
    
    def table_vide(self):
        lt = []
        for table in self.liste_tables:
            if not table.liste_comptes == []:
                lt.append(table)
        self.liste_tables = lt

    def afficher(self) -> str:
        """Afficher les informations de connexion"""
        res = "Actuellement en session :\n"
        res += "-------------------------\n"
        for att in list(self.__dict__.items()):
            res += f"{att[0]} : {att[1]}\n"

        return res
