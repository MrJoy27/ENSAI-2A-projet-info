from .carte import Carte, Couleur, Valeur
from .liste_cartes import ListeCartes

from typing import Iterable, Dict, List, Any, Optional
import random

class DeckVideError(Exception):
    """Levée quand on demande plus de cartes qu'il n'en reste dans le paquet."""


class OrdreDistributionError(Exception):
    """Levée si on ne respecte pas la séquence Hold'em (préflop → flop → turn → river)."""


class Deck:
    """
    Représente un paquet standard de 52 cartes pour le Texas Hold’em.

    Fonctions principales :
      - reinitialiser() : reconstruit le paquet complet (52 cartes) et vide les brûlées
      - melanger(seed)  : mélange le paquet (déterministe si une seed est donnée)
      - piocher(n)      : pioche n cartes (du dessus du paquet)
      - distribuer_cartes_privees(joueurs)
      - donner_flop() / donner_turn() / donner_river()
    """

    __slots__ = ("_paquet", "_brulees", "_etat", "_seed")

    def __init__(self, seed: Optional[int] = None) -> None:
        self._seed: Optional[int] = seed
        self._paquet: List[Carte] = []
        self._brulees: List[Carte] = []
        self._etat: str = "new"  # "new" -> "preflop" -> "flop" -> "turn" -> "river" -> "done"
        self.reinitialiser()
        self.melanger(seed=seed)

    @staticmethod
    def _generer_paquet_52() -> List[Carte]:
        ordre_valeurs = [
            Valeur.Deux, Valeur.Trois, Valeur.Quatre, Valeur.Cinq, Valeur.Six, Valeur.Sept,
            Valeur.Huit, Valeur.Neuf, Valeur.Dix, Valeur.Valet, Valeur.Dame, Valeur.Roi, Valeur.As
        ]
        ordre_couleurs = [Couleur.Pique, Couleur.Carreau, Couleur.Coeur, Couleur.Trefle]
        return [Carte(v, c) for c in ordre_couleurs for v in ordre_valeurs]

    def reinitialiser(self) -> None:
        """Reconstruit le paquet complet et réinitialise l’état."""
        self._paquet = self._generer_paquet_52()
        self._brulees = []
        self._etat = "preflop"

    def cartes_restantes(self) -> int:
        return len(self._paquet)

    def cartes_brulees(self) -> ListeCartes:
        return ListeCartes(self._brulees[:])

    def piocher(self, n: int = 1) -> List[Carte]:
        """Pioche n cartes du dessus du paquet (lève DeckVideError si pas assez)."""
        if n < 0:
            raise ValueError("n doit être ≥ 0.")
        if n > len(self._paquet):
            raise DeckVideError(f"Demande {n} cartes, mais il reste {len(self._paquet)} carte(s).")
        if n == 0:
            return []
        sorties = self._paquet[-n:]
        del self._paquet[-n:]
        return sorties

    def bruler(self) -> Carte:
        """Brûle une carte (la retire définitivement du paquet)."""
        c = self.piocher(1)[0]
        self._brulees.append(c)
        return c

    def distribuer_cartes_privees(self, joueurs: Iterable[Any]) -> Dict[Any, ListeCartes]:
        """
        Donne 2 cartes à chaque joueur en alternance (préflop).
        Renvoie un dict {joueur: ListeCartes([c1, c2])}.
        """
        if self._etat != "preflop":
            raise OrdreDistributionError("Les cartes privatives ne peuvent être distribuées qu'en préflop.")

        joueurs = list(joueurs)
        if len(joueurs) < 2:
            raise ValueError("Au moins 2 joueurs sont nécessaires pour distribuer les cartes privatives.")
        mains: Dict[Any, List[Carte]] = {j: [] for j in joueurs}
        for j in joueurs:
            mains[j].extend(self.piocher(1))
        for j in joueurs:
            mains[j].extend(self.piocher(1))

        mains_liste = {j: ListeCartes(mains[j]) for j in joueurs}
        self._etat = "flop"
        return mains_liste

    def donner_flop(self) -> ListeCartes:
        if self._etat != "flop":
            raise OrdreDistributionError("Le flop ne peut être donné qu'après le préflop.")
        self.bruler()
        flop = self.piocher(3)
        self._etat = "turn"
        return ListeCartes(flop)

    def donner_turn(self) -> Carte:
        if self._etat != "turn":
            raise OrdreDistributionError("Le turn ne peut être donné qu'après le flop.")
        self.bruler()
        turn = self.piocher(1)[0]
        self._etat = "river"
        return turn

    def donner_river(self) -> Carte:
        if self._etat != "river":
            raise OrdreDistributionError("La river ne peut être donnée qu'après le turn.")
        self.bruler()
        river = self.piocher(1)[0]
        self._etat = "done"
        return river