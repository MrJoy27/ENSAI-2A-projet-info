"""Implémentation de la classe Carte."""


class Carte:

    """
     une carte, composée d'une couleur et d'une valeur

    """

    __VALEURS = ('As', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                 'Valet', 'Dame', 'Roi')
    __COULEURS = ('Pique', 'Carreau', 'Coeur', 'Trêfle')

    def __init__(self, valeur: str, couleur: str):
        if valeur not in Carte.__VALEURS:
            raise ValueError("valeur non valide")
        if couleur not in Carte.__COULEURS:
            raise ValueError("couleur non valide")
        self.__valeur = valeur
        self.__couleur = couleur

    @classmethod
    def VALEURS(classe):
        return classe.__VALEURS

    @classmethod
    def COULEURS(classe):
        return classe.__COULEURS

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
