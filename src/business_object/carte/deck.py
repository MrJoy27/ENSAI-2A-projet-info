from .carte import Carte, Couleur, Valeur
from .liste_cartes import ListeCartes

from typing import Iterable, Dict, List, Any, Optional
import random

class DeckVideError(Exception):


class OrdreDistributionError(Exception):


class Deck:

    __slots__ = ("_paquet", "_brulees", "_etat", "_seed")

    def __init__(self, seed: Optional[int] = None) -> None:
        self._seed: Optional[int] = seed
        self._paquet: List[Carte] = []
        self.melanger(seed=seed)

    @staticmethod
    def _generer_paquet_52() -> List[Carte]:
        ordre_valeurs = [
            Valeur.Deux, Valeur.Trois, Valeur.Quatre, Valeur.Cinq, Valeur.Six, Valeur.Sept,
            Valeur.Huit, Valeur.Neuf, Valeur.Dix, Valeur.Valet, Valeur.Dame, Valeur.Roi, Valeur.As
        ]
        ordre_couleurs = [Couleur.Pique, Couleur.Carreau, Couleur.Coeur, Couleur.Trefle]
        return [Carte(v, c) for c in ordre_couleurs for v in ordre_valeurs]
    def piocher(self, n: int = 1) -> List[Carte]:
        if n < 0:
            raise ValueError("n doit être ≥ 0.")
        if n > len(self._paquet):
            raise DeckVideError(f"Demande {n} cartes, mais il reste {len(self._paquet)} carte(s).")
        if n == 0:
            return []
        sorties = self._paquet[-n:]
        del self._paquet[-n:]
        return sorties
    def melanger(self, seed: Optional[int] = None) -> None:    
        self._paquet = self._generer_paquet_52()
        if seed is not None:
            random.seed(seed)
        random.shuffle(self._paquet)
        