import pytest
from business_object.carte.carte import Carte, Valeur, Couleur
from business_object.carte.liste_cartes import ListeCartes


def test_init_valide():
    cartes = [Carte(Valeur.As, Couleur.Carreau), Carte(Valeur.Roi, Couleur.Pique)]
    liste = ListeCartes(cartes)
    assert len(liste) == 2
    assert liste.cartes[0] == cartes[0]


def test_init_invalide_type():
    with pytest.raises(ValueError):
        ListeCartes("pas une liste")


def test_init_invalide_contenu():
    with pytest.raises(ValueError):
        ListeCartes([42, "X"])


def test_eq_egalite():
    cartes1 = [Carte(Valeur.As, Couleur.Carreau)]
    cartes2 = [Carte(Valeur.As, Couleur.Carreau)]
    assert ListeCartes(cartes1) == ListeCartes(cartes2)


def test_eq_different():
    cartes1 = [Carte(Valeur.As, Couleur.Carreau)]
    cartes2 = [Carte(Valeur.Roi, Couleur.Coeur)]
    assert ListeCartes(cartes1) != ListeCartes(cartes2)


def test_str():
    liste = ListeCartes([Carte(Valeur.As, Couleur.Carreau)])
    assert str(liste) == "[As de Carreau]"  # adapter si ton __str__ de Carte affiche différemment


def test_len():
    liste = ListeCartes([Carte(Valeur.As, Couleur.Carreau),
                         Carte(Valeur.Roi, Couleur.Pique)])
    assert len(liste) == 2


def test_ajouter_carte():
    liste = ListeCartes([])
    liste.ajouter_carte(Carte(Valeur.As, Couleur.Carreau))
    assert len(liste) == 1


def test_ajouter_carte_mauvais_type():
    liste = ListeCartes([])
    with pytest.raises(TypeError):
        liste.ajouter_carte("pas une carte")


def test_retirer_carte():
    carte = Carte(Valeur.As, Couleur.Carreau)
    liste = ListeCartes([carte])
    retirée = liste.retirer_carte(0)
    assert retirée == carte
    assert len(liste) == 0


def test_retirer_carte_liste_vide():
    liste = ListeCartes([])
    with pytest.raises(Exception):
        liste.retirer_carte(0)


def test_retirer_carte_indice_invalide():
    liste = ListeCartes([Carte(Valeur.As, Couleur.Carreau)])
    with pytest.raises(ValueError):
        liste.retirer_carte(10)


def test_max():
    liste = ListeCartes([
        Carte(Valeur.Quatre, Couleur.Coeur),
        Carte(Valeur.As, Couleur.Carreau)
    ])
    assert liste.max() == Carte(Valeur.As, Couleur.Carreau)
