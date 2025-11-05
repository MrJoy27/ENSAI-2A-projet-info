import pytest
from deck import Deck, DeckVideError
from carte import Carte, Couleur, Valeur


def test_melanger_recree_paquet_52():
    """Vérifie que melanger() crée un paquet de 52 cartes."""
    deck = Deck()
    assert len(deck._paquet) == 52, "Le paquet doit contenir 52 cartes après mélange."


def test_melanger_avec_seed_identique():
    """Deux decks avec la même seed doivent avoir le même ordre."""
    deck1 = Deck(seed=42)
    deck2 = Deck(seed=42)
    assert deck1._paquet == deck2._paquet, "Les paquets doivent être identiques avec la même seed."


def test_melanger_avec_seed_differente():
    """Deux decks avec des seeds différentes doivent avoir un ordre différent."""
    deck1 = Deck(seed=1)
    deck2 = Deck(seed=2)
    assert deck1._paquet != deck2._paquet, "Les paquets doivent différer avec des seeds différentes."


def test_melanger_modifie_ordre():
    """Le mélange doit changer l'ordre par rapport à l'ordre naturel."""
    deck = Deck()
    original_order = deck._generer_paquet_52()
    deck.melanger()
    assert deck._paquet != original_order, "Le mélange doit modifier l'ordre des cartes."


def test_piocher_retourne_bonnes_cartes():
    """Vérifie que piocher() retire bien les cartes du paquet."""
    deck = Deck(seed=123)
    taille_initiale = len(deck._paquet)
    cartes_piochees = deck.piocher(3)
    assert len(cartes_piochees) == 3, "Doit piocher 3 cartes."
    assert len(deck._paquet) == taille_initiale - 3, "Le paquet doit être réduit de 3 cartes."


def test_piocher_plus_que_restantes_declenche_erreur():
    """Vérifie que piocher trop de cartes déclenche une erreur."""
    deck = Deck()
    with pytest.raises(DeckVideError):
        deck.piocher(60)


def test_piocher_zero_cartes():
    """Vérifie qu'on peut piocher zéro carte sans erreur."""
    deck = Deck()
    result = deck.piocher(0)
    assert result == [], "Piocher 0 carte doit retourner une liste vide."
    assert len(deck._paquet) == 52, "Le paquet ne doit pas être modifié."