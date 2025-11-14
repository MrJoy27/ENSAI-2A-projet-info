from .carte import Carte, Couleur, Valeur
from .liste_cartes import ListeCartes


class Deck:

    def __init__(self):
        ordre_valeurs = [
            Valeur.Deux, Valeur.Trois, Valeur.Quatre, Valeur.Cinq, Valeur.Six, Valeur.Sept,
            Valeur.Huit, Valeur.Neuf, Valeur.Dix, Valeur.Valet, Valeur.Dame, Valeur.Roi, Valeur.As
        ]
        ordre_couleurs = [Couleur.Pique, Couleur.Carreau, Couleur.Coeur, Couleur.Trefle]
        self.cartes = ListeCartes([Carte(v, c) for c in ordre_couleurs for v in ordre_valeurs])

    def piocher(self):
        return self.cartes.retirer_carte(len(self.cartes)-1)

    def melanger(self, seed = None):
        self.cartes.melanger()
        