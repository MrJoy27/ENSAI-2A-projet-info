from dao.admin_dao import adminDao
from business_object.compte import Compte
from business_object.admin import Admin
from unittest.mock import MagicMock
import pytest


def test_trouverid_ok():
    """Tester si on peut trouver un compte par son id"""

    # GIVEN
    id_compte = 1234
    expected = Compte(
        nom="pikachu", 
        nb_jetons=999, 
        nb_victoires=5, 
        nb_parties=20000
    )
    adminDao().trouver_par_id = MagicMock(return_value=expected)
     
    # WHEN
    compte = adminDao().trouver_par_id(id_compte)

    # THEN
    assert isinstance(compte, Compte)
    assert compte.nom == expected.nom
    assert compte.nb_jetons == expected.nb_jetons
    assert compte.nb_victoires == expected.nb_victoires
    assert compte.nb_parties == expected.nb_parties



def test_lister_ok():
    """Test si l'admin peut lister tous les comptes"""

    # GIVEN
    expected_comptes = [
        Compte(nom="tartiflette", nb_jetons=5000, nb_victoires=122, nb_parties=122),
        Compte(nom="princesse", nb_jetons=800123000, nb_victoires=0, nb_parties=0),
    ]

    adminDao().lister_tous = MagicMock(return_value=expected_comptes)

    # WHEN
    comptes = adminDao().lister_tous()

    # THEN
    assert len(comptes) == 2
    assert comptes[0].nom == "tartiflette"
    assert comptes[1].nom == "princesse"



def test_crediter_ok():
    """Test si l'admin peut créditer des jetons aux joueurs """

    # GIVEN
    id_compte = 1234
    nb_jetons = 500
    res = True

    adminDao().crediter = MagicMock(return_value=res)

    # WHEN
    result = adminDao().crediter(id_compte, nb_jetons)

    # THEN
    assert result == res



def test_supp_ok():
    """Test si la suppression d'un compte fonctionne"""

    # GIVEN
    id_compte = 28
    rep = True

    adminDao().supprimer = MagicMock(return_value=rep)

    # WHEN
    res = adminDao().supprimer(id_compte)

    # THEN
    assert res == rep



def test_se_connecter_ok():
    """Test si l'admin peut se connecter avec son nom et son mot de passe correctement'"""

    # GIVEN
    nom = "tartiflette"
    mdp = "secret123"
    expected_admin = Admin(nom="tartiflette", mdp="secret123")

    adminDao().se_connecter = MagicMock(return_value=expected_admin)

    # WHEN
    admin = adminDao().se_connecter(nom, mdp)

    # THEN
    assert isinstance(admin, Admin)
    assert admin.nom == expected_admin.nom
    assert admin.mdp == expected_admin.mdp

