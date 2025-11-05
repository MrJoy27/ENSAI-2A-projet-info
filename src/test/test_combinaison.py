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


def test_double_paire_egales():
    """Deux doubles paires identiques doivent être considérées égales."""
    main1 = [
        Carte(Valeur.As, Couleur.Carreau),
        Carte(Valeur.As, Couleur.Coeur),
        Carte(Valeur.Roi, Couleur.Trefle),
        Carte(Valeur.Roi, Couleur.Pique),
        Carte(Valeur.Dix, Couleur.Coeur)
    ]
    main2 = [
        Carte(Valeur.As, Couleur.Trefle),
        Carte(Valeur.As, Couleur.Pique),
        Carte(Valeur.Roi, Couleur.Carreau),
        Carte(Valeur.Roi, Couleur.Coeur),
        Carte(Valeur.Dix, Couleur.Trefle)
    ]
    combinaison1 = Combinaison(main1)
    combinaison2 = Combinaison(main2)

    assert combinaison1 == combinaison2
    assert not (combinaison1 != combinaison2)
    assert not (combinaison1 < combinaison2)
    assert not (combinaison1 > combinaison2)
    assert combinaison1 <= combinaison2
    assert combinaison1 >= combinaison2


def test_double_paire_plus_forte():
    """Une double paire avec des valeurs plus hautes doit être supérieure."""
    main_forte = [
        Carte(Valeur.As, Couleur.Carreau),
        Carte(Valeur.As, Couleur.Coeur),
        Carte(Valeur.Roi, Couleur.Trefle),
        Carte(Valeur.Roi, Couleur.Pique),
        Carte(Valeur.Dix, Couleur.Coeur)
    ]
    main_faible = [
        Carte(Valeur.Dame, Couleur.Carreau),
        Carte(Valeur.Dame, Couleur.Coeur),
        Carte(Valeur.Valet, Couleur.Trefle),
        Carte(Valeur.Valet, Couleur.Pique),
        Carte(Valeur.Huit, Couleur.Coeur)
    ]
    combinaison_forte = Combinaison(main_forte)
    combinaison_faible = Combinaison(main_faible)

    assert combinaison_forte > combinaison_faible
    assert combinaison_faible < combinaison_forte
    assert not (combinaison_forte < combinaison_faible)
    assert not (combinaison_faible > combinaison_forte)


def test_paire_meme_type_mais_carte_plus_haute():
    """Deux paires d’un même type : celle avec la paire la plus haute gagne."""
    main_paire_as = [
        Carte(Valeur.As, Couleur.Carreau),
        Carte(Valeur.As, Couleur.Coeur),
        Carte(Valeur.Dix, Couleur.Pique),
        Carte(Valeur.Huit, Couleur.Trefle),
        Carte(Valeur.Quatre, Couleur.Coeur)
    ]
    main_paire_dame = [
        Carte(Valeur.Dame, Couleur.Carreau),
        Carte(Valeur.Dame, Couleur.Coeur),
        Carte(Valeur.Dix, Couleur.Trefle),
        Carte(Valeur.Huit, Couleur.Pique),
        Carte(Valeur.Quatre, Couleur.Coeur)
    ]
    combinaison_as = Combinaison(main_paire_as)
    combinaison_dame = Combinaison(main_paire_dame)

    assert combinaison_as > combinaison_dame
    assert combinaison_dame < combinaison_as
    assert not (combinaison_as < combinaison_dame)


def test_quinte_haute_vs_quinte_basse():
    """Une quinte plus haute doit battre une quinte plus basse."""
    main_quinte_basse = [
        Carte(Valeur.Cinq, Couleur.Carreau),
        Carte(Valeur.Six, Couleur.Pique),
        Carte(Valeur.Sept, Couleur.Coeur),
        Carte(Valeur.Huit, Couleur.Trefle),
        Carte(Valeur.Neuf, Couleur.Coeur)
    ]
    main_quinte_haute = [
        Carte(Valeur.Huit, Couleur.Carreau),
        Carte(Valeur.Neuf, Couleur.Pique),
        Carte(Valeur.Dix, Couleur.Coeur),
        Carte(Valeur.Valet, Couleur.Trefle),
        Carte(Valeur.Dame, Couleur.Coeur)
    ]
    combinaison_basse = Combinaison(main_quinte_basse)
    combinaison_haute = Combinaison(main_quinte_haute)

    assert combinaison_haute > combinaison_basse
    assert combinaison_basse < combinaison_haute


def test_full_egaux():
    """Deux fulls avec les mêmes valeurs (brelan et paire identiques) sont égaux."""
    main1 = [
        Carte(Valeur.Roi, Couleur.Carreau),
        Carte(Valeur.Roi, Couleur.Coeur),
        Carte(Valeur.Roi, Couleur.Pique),
        Carte(Valeur.Dame, Couleur.Trefle),
        Carte(Valeur.Dame, Couleur.Carreau)
    ]
    main2 = [
        Carte(Valeur.Roi, Couleur.Trefle),
        Carte(Valeur.Roi, Couleur.Coeur),
        Carte(Valeur.Roi, Couleur.Carreau),
        Carte(Valeur.Dame, Couleur.Pique),
        Carte(Valeur.Dame, Couleur.Coeur)
    ]
    combinaison1 = Combinaison(main1)
    combinaison2 = Combinaison(main2)

    assert combinaison1 == combinaison2
    assert not (combinaison1 < combinaison2)
    assert not (combinaison1 > combinaison2)

def test_paire_superieure_a_hauteur():
    main1 = [
        Carte(Valeur.As, Couleur.Carreau),
        Carte(Valeur.As, Couleur.Coeur),
        Carte(Valeur.Dix, Couleur.Trefle),
        Carte(Valeur.Neuf, Couleur.Pique),
        Carte(Valeur.Huit, Couleur.Coeur)
    ]
    main2 = [
        Carte(Valeur.Deux, Couleur.Carreau),
        Carte(Valeur.Cinq, Couleur.Trefle),
        Carte(Valeur.Sept, Couleur.Coeur),
        Carte(Valeur.Valet, Couleur.Pique),
        Carte(Valeur.Roi, Couleur.Coeur)
    ]
    combinaison_paire = Combinaison(main1)
    combinaison_hauteur = Combinaison(main2)
    assert combinaison_paire > combinaison_hauteur
    assert not (combinaison_paire < combinaison_hauteur)

def test_brelan_superieur_a_double_paire():
    main_brelan = [
        Carte(Valeur.Dame, Couleur.Carreau),
        Carte(Valeur.Dame, Couleur.Coeur),
        Carte(Valeur.Dame, Couleur.Trefle),
        Carte(Valeur.Sept, Couleur.Pique),
        Carte(Valeur.Cinq, Couleur.Carreau)
    ]
    main_double_paire = [
        Carte(Valeur.Roi, Couleur.Carreau),
        Carte(Valeur.Roi, Couleur.Coeur),
        Carte(Valeur.Dix, Couleur.Trefle),
        Carte(Valeur.Dix, Couleur.Pique),
        Carte(Valeur.Quatre, Couleur.Coeur)
    ]
    combinaison_brelan = Combinaison(main_brelan)
    combinaison_double_paire = Combinaison(main_double_paire)
    assert combinaison_brelan > combinaison_double_paire

def test_quinte_flush_royale_superieure_a_tout():
    main_quinte_flush_royale = [
        Carte(Valeur.Dix, Couleur.Coeur),
        Carte(Valeur.Valet, Couleur.Coeur),
        Carte(Valeur.Dame, Couleur.Coeur),
        Carte(Valeur.Roi, Couleur.Coeur),
        Carte(Valeur.As, Couleur.Coeur)
    ]
    main_full = [
        Carte(Valeur.As, Couleur.Carreau),
        Carte(Valeur.As, Couleur.Trefle),
        Carte(Valeur.As, Couleur.Pique),
        Carte(Valeur.Roi, Couleur.Coeur),
        Carte(Valeur.Roi, Couleur.Trefle)
    ]
    combinaison_qfr = Combinaison(main_quinte_flush_royale)
    combinaison_full = Combinaison(main_full)
    assert combinaison_qfr > combinaison_full
    assert not (combinaison_qfr < combinaison_full)

def test_egalite_meme_combinaison_meme_valeur():
    main1 = [
        Carte(Valeur.As, Couleur.Carreau),
        Carte(Valeur.As, Couleur.Coeur),
        Carte(Valeur.Dix, Couleur.Trefle),
        Carte(Valeur.Neuf, Couleur.Pique),
        Carte(Valeur.Huit, Couleur.Coeur)
    ]
    main2 = [
        Carte(Valeur.As, Couleur.Pique),
        Carte(Valeur.As, Couleur.Trefle),
        Carte(Valeur.Dix, Couleur.Carreau),
        Carte(Valeur.Neuf, Couleur.Coeur),
        Carte(Valeur.Huit, Couleur.Pique)
    ]
    combinaison1 = Combinaison(main1)
    combinaison2 = Combinaison(main2)
    assert combinaison1 == combinaison2
    assert not (combinaison1 != combinaison2)