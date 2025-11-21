import pytest
from business_object.carte.deck import Deck
from business_object.carte.carte import Carte, Valeur, Couleur


def test_deck_initialisation():
    deck = Deck()
    assert len(deck.cartes) == 52

    # Vérifie que toutes les cartes sont uniques
    set_cartes = set(deck.cartes)
    assert len(set_cartes) == 52


def test_deck_ordre_initial():
    deck = Deck()

    ordre_valeurs = [
        Valeur.Deux, Valeur.Trois, Valeur.Quatre, Valeur.Cinq, Valeur.Six, Valeur.Sept,
        Valeur.Huit, Valeur.Neuf, Valeur.Dix, Valeur.Valet, Valeur.Dame, Valeur.Roi, Valeur.As
    ]
    ordre_couleurs = [Couleur.Pique, Couleur.Carreau, Couleur.Coeur, Couleur.Trefle]

    # Reconstruction manuelle du deck attendu
    expected = [Carte(v, c) for c in ordre_couleurs for v in ordre_valeurs]

    assert deck.cartes == expected


def test_piocher_retire_derniere_carte():
    deck = Deck()
    last_card = deck.cartes[-1]
    piochée = deck.piocher()

    assert piochée == last_card
    assert len(deck.cartes) == 51
    assert last_card not in deck.cartes


def test_piocher_plusieurs():
    deck = Deck()
    initial_len = len(deck.cartes)

    c1 = deck.piocher()
    c2 = deck.piocher()

    assert len(deck.cartes) == initial_len - 2
    assert c1 != c2
    assert c1 not in deck.cartes
    assert c2 not in deck.cartes


def test_piocher_deck_vide():
    deck = Deck()
    for _ in range(52):
        deck.piocher()

    with pytest.raises(Exception):
        deck.piocher()


def test_deck_melanger_change_ordre():
    deck = Deck()
    original = deck.cartes.copy()

    deck.melanger()

    # On vérifie qu'au moins une carte n'est plus à la même position
    assert deck.cartes != original


def test_deck_melanger_pas_de_perte():
    deck = Deck()
    deck.melanger()

    assert len(deck.cartes) == 52
    assert len(set(deck.cartes)) == 52