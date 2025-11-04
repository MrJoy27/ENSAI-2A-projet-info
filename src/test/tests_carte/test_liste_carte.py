from business_object.carte.carte import Carte, Valeur, Couleur
from business_object.carte.liste_cartes import ListeCartes
import pytest

def test_max():
    liste=ListeCartes([Carte(Valeur.As,Couleur.Carreau),Carte(Valeur.Quatre,Couleur.Coeur)])
    assert liste.max()==Carte(Valeur.As,Couleur.Carreau)