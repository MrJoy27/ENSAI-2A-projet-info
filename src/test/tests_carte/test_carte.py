from business_object.carte.carte import Carte, Valeur, Couleur
import pytest

def test_valeur():
    Card = Carte(Valeur.Deux, Couleur.Pique)
    assert Card.valeur == 'Deux'

def test_couleur():
    Card = Carte(Valeur.Six, Couleur.Pique)
    assert Card.couleur == 'Pique'

def test_str():
    Card = Carte(Valeur.Roi, Couleur.Coeur)
    assert str(Card) == "Roi de Coeur"

def test_repr():
    Card = Carte(Valeur.Dame, Couleur.Carreau)
    assert repr(Card) == "Carte(Valeur.Dame, Couleur.Carreau)"

def test_eq():
    Card1 = Carte(Valeur.Deux, Couleur.Pique)
    Card2 = Carte(Valeur.Deux, Couleur.Pique)
    assert Card1 == Card2


def test_hash():
    Card = Carte(Valeur.Trois, Couleur.Pique)
    assert hash(Card) == hash((Valeur.Trois, Couleur.Pique))

def test_comp():
    Card1 = Carte(Valeur.Trois, Couleur.Pique)
    Card2 = Carte(Valeur.Sept, Couleur.Carreau)
    assert Card1 < Card2
def test_max():
    liste=[Carte(Valeur.Cinq,Couleur.Pique), Carte(Valeur.Sept, Couleur.Carreau), Carte(Valeur.As, Couleur.Carreau)]
    max_liste=max(liste)
    assert max_liste==Carte(Valeur.As, Couleur.Carreau)
if __name__ == "__main__":
    pytest.main([__file__])