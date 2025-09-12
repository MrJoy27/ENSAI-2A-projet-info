"""Implémentation de la classe Carte."""

from enum import Enum

class Couleur(Enum):
    Coeur = "Coeur"
    Pique = "Pique"
    Carreau = "Carreau"
    Trefle = "Trefle"

class Valeur(Enum):
    As = "As"
    Deux = "2"
    Trois = "3"
    Quatre = "4"
    Cinq = "5"
    Six = "6"
    Sept = "7"
    Huit = "8"
    Neuf = "9"
    Dix = "10"
    Valet = "Valet"
    Dame = "Dame"
    Roi = "Roi"


class Carte:

    """
     une carte, composée d'une couleur et d'une valeur

    """

    def __init__(self, valeur: Valeur, couleur: Couleur):
        if isinstance(valeur, Valeur):
            raise ValueError("valeur non valide")
        if isinstance(couleur, Couleur):
            raise ValueError("couleur non valide")
        self.__valeur = valeur
        self.__couleur = couleur

    @property
    def valeur(self):
        return self.__valeur

    @property
    def couleur(self):
        return self.__couleur

    def __str__(self):
        return f"{self.__valeur} de {self.__couleur.lower()}"

    def __repr__(self):
        return f"Carte('{self.__valeur}','{self.__couleur}')"

    def __eq__(self, card):
        if not isinstance(card, Carte):
            raise TypeError("l'argument doit être une carte")
        return self.__valeur == card.__valeur and self.__couleur == card.__couleur

    def __hash__(self):
        return hash((self.__valeur, self.__couleur))
