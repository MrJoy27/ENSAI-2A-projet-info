import pytest
from business_object.carte.carte import Carte, Valeur, Couleur
from business_object.combinaison import Combinaison  # vérifie que le chemin est correct


def test_quinte_flush_royale():
    main = [
        Carte(Valeur.Dix, Couleur.Coeur),
        Carte(Valeur.Valet, Couleur.Coeur),
        Carte(Valeur.Dame, Couleur.Coeur),
        Carte(Valeur.Roi, Couleur.Coeur),
        Carte(Valeur.As, Couleur.Coeur)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Quinte Flush Royale"


def test_quinte_flush():
    main = [
        Carte(Valeur.Six, Couleur.Pique),
        Carte(Valeur.Sept, Couleur.Pique),
        Carte(Valeur.Huit, Couleur.Pique),
        Carte(Valeur.Neuf, Couleur.Pique),
        Carte(Valeur.Dix, Couleur.Pique)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Quinte Flush"


def test_carre():
    main = [
        Carte(Valeur.As, Couleur.Trefle),
        Carte(Valeur.As, Couleur.Coeur),
        Carte(Valeur.As, Couleur.Pique),
        Carte(Valeur.As, Couleur.Carreau),
        Carte(Valeur.Roi, Couleur.Coeur)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Carré"


def test_full():
    main = [
        Carte(Valeur.Dame, Couleur.Trefle),
        Carte(Valeur.Dame, Couleur.Coeur),
        Carte(Valeur.Dame, Couleur.Carreau),
        Carte(Valeur.Neuf, Couleur.Trefle),
        Carte(Valeur.Neuf, Couleur.Coeur)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Full"


def test_couleur():
    main = [
        Carte(Valeur.Deux, Couleur.Carreau),
        Carte(Valeur.Cinq, Couleur.Carreau),
        Carte(Valeur.Neuf, Couleur.Carreau),
        Carte(Valeur.Valet, Couleur.Carreau),
        Carte(Valeur.Roi, Couleur.Carreau)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Couleur"


def test_quinte():
    main = [
        Carte(Valeur.Cinq, Couleur.Trefle),
        Carte(Valeur.Six, Couleur.Coeur),
        Carte(Valeur.Sept, Couleur.Carreau),
        Carte(Valeur.Huit, Couleur.Pique),
        Carte(Valeur.Neuf, Couleur.Trefle)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Quinte"


def test_brelan():
    main = [
        Carte(Valeur.Valet, Couleur.Carreau),
        Carte(Valeur.Valet, Couleur.Trefle),
        Carte(Valeur.Valet, Couleur.Coeur),
        Carte(Valeur.Trois, Couleur.Carreau),
        Carte(Valeur.Sept, Couleur.Pique)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Brelan"


def test_double_paire():
    main = [
        Carte(Valeur.Dix, Couleur.Carreau),
        Carte(Valeur.Dix, Couleur.Trefle),
        Carte(Valeur.Roi, Couleur.Coeur),
        Carte(Valeur.Roi, Couleur.Pique),
        Carte(Valeur.Deux, Couleur.Coeur)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Double Paire"


def test_paire():
    main = [
        Carte(Valeur.Six, Couleur.Carreau),
        Carte(Valeur.Six, Couleur.Trefle),
        Carte(Valeur.Dix, Couleur.Coeur),
        Carte(Valeur.Valet, Couleur.Pique),
        Carte(Valeur.Roi, Couleur.Coeur)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Paire"


def test_hauteur():
    main = [
        Carte(Valeur.Deux, Couleur.Carreau),
        Carte(Valeur.Cinq, Couleur.Trefle),
        Carte(Valeur.Sept, Couleur.Coeur),
        Carte(Valeur.Valet, Couleur.Pique),
        Carte(Valeur.Roi, Couleur.Coeur)
    ]
    combinaison = Combinaison(main)
    assert combinaison.type == "Hauteur"
