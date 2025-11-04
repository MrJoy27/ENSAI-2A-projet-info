import pytest
from carte import Carte, ListeCartes, Combinaison

def test_quinte_flush_royale():
    main = ListeCartes([
        Carte("Dix", "Coeur"),
        Carte("Valet", "Coeur"),
        Carte("Dame", "Coeur"),
        Carte("Roi", "Coeur"),
        Carte("As", "Coeur")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Quinte Flush Royale"

def test_quinte_flush():
    main = ListeCartes([
        Carte("Six", "Pique"),
        Carte("Sept", "Pique"),
        Carte("Huit", "Pique"),
        Carte("Neuf", "Pique"),
        Carte("Dix", "Pique")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Quinte Flush"

def test_carre():
    main = ListeCartes([
        Carte("As", "Trefle"),
        Carte("As", "Coeur"),
        Carte("As", "Pique"),
        Carte("As", "Carreau"),
        Carte("Roi", "Coeur")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Carré"

def test_full():
    main = ListeCartes([
        Carte("Dame", "Trefle"),
        Carte("Dame", "Coeur"),
        Carte("Dame", "Carreau"),
        Carte("Neuf", "Trefle"),
        Carte("Neuf", "Coeur")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Full"

def test_couleur():
    main = ListeCartes([
        Carte("Deux", "Carreau"),
        Carte("Cinq", "Carreau"),
        Carte("Neuf", "Carreau"),
        Carte("Valet", "Carreau"),
        Carte("Roi", "Carreau")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Couleur"

def test_quinte():
    main = ListeCartes([
        Carte("Cinq", "Trefle"),
        Carte("Six", "Coeur"),
        Carte("Sept", "Carreau"),
        Carte("Huit", "Pique"),
        Carte("Neuf", "Trefle")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Quinte"

def test_brelan():
    main = ListeCartes([
        Carte("Valet", "Carreau"),
        Carte("Valet", "Trefle"),
        Carte("Valet", "Coeur"),
        Carte("Trois", "Carreau"),
        Carte("Sept", "Pique")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Brelan"

def test_double_paire():
    main = ListeCartes([
        Carte("Dix", "Carreau"),
        Carte("Dix", "Trefle"),
        Carte("Roi", "Coeur"),
        Carte("Roi", "Pique"),
        Carte("Deux", "Coeur")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Double Paire"

def test_paire():
    main = ListeCartes([
        Carte("Six", "Carreau"),
        Carte("Six", "Trefle"),
        Carte("Dix", "Coeur"),
        Carte("Valet", "Pique"),
        Carte("Roi", "Coeur")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Paire"

def test_hauteur():
    main = ListeCartes([
        Carte("Deux", "Carreau"),
        Carte("Cinq", "Trefle"),
        Carte("Sept", "Coeur"),
        Carte("Valet", "Pique"),
        Carte("Roi", "Coeur")
    ])
    combinaison = Combinaison(main)
    assert combinaison.type == "Hauteur"