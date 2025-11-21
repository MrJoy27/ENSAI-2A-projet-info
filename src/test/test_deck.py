import pytest
from business_object.carte.deck import Deck
from business_object.carte.carte import Carte, Valeur, Couleur

def test_piocher_deck_vide():
    deck = Deck()
    for _ in range(52):
        deck.piocher()

    with pytest.raises(Exception):
        deck.piocher()
