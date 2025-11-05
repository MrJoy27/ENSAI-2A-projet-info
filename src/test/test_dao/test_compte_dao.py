from dao.compte_dao import compteDao
from business_object.compte import Compte
from unittest.mock import MagicMock
import pytest 

def test_creer_ok():
    """ création des comptes ok """

    # GIVEN
    nom, mdp = "tartiflette", "password123"
    expected= True
    compteDao().creer = MagicMock(return_value=expected)

    # WHEN
    result = compteDao().creer(nom, mdp)

    # THEN
    assert result == expected

def test_modifier_ok():
    """ tester si le joueur peut modifier son mdp """

    # GIVEN
    compte = Compte(nom="tartiflette", mdp="newpassword123")
    compte.id = 1256
    expected = True  
    compteDao().modifier = MagicMock(return_value=expected)

    # WHEN
    result = compteDao().modifier(compte)

    # THEN
    assert result == expected


def test_supp_ok():
    """ tester si le joueur peut supprimer SON compte"""

    # GIVEN
    compte = Compte(nom="tartif", mdp="password123")
    expected = True 
    compteDao().supprimer = MagicMock(return_value=expected)

    # WHEN
    result = compteDao().supprimer(compte)

    # THEN
    assert result == expected



def test2_supp_not_ok():
    """Tester que si tu n'as pas les bons identifiants un compte ne sera pas supprimé"""

    # GIVEN
    compte = Compte(nom="tartiflette", mdp="password123")
    mauvais_mdp = "mauvais_mdp"  
    compteDao().supprimer = MagicMock(return_value=False)  

    # WHEN
    result = compteDao().supprimer(compte, mauvais_mdp) 

    # THEN
    assert result == False 



def test_connexion_ok():
    """tester si un joueur peut se connecter facilement à son compte avec son pseudo et son mdp"""
    # GIVEN
    nom, mdp = "toutou", "password123"
    expected_compte = Compte(nom=nom, mdp=mdp, nb_jetons=10, nb_victoires=5, nb_parties=20)
    compteDao().se_connecter = MagicMock(return_value=expected_compte)

    # WHEN
    compte = compteDao().se_connecter(nom, mdp)

    # THEN
    assert isinstance(compte, Compte)
    assert compte.nom == expected_compte.nom
    assert compte.mdp == expected_compte.mdp
    assert compte.nb_jetons == expected_compte.nb_jetons
    assert compte.nb_victoires == expected_compte.nb_victoires
    assert compte.nb_parties == expected_compte.nb_parties
