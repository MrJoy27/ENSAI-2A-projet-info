import pytest
from business_object.joueur import Joueur
from business_object.carte.carte import Carte, Valeur, Couleur

class FakeManche:
    def __init__(self, joueurs, mise=10):
        self.liste_joueurs = joueurs
        self.pot = 0
        self.mise = mise
        self.tour = 0
        self.n = len(joueurs)
        self.couche = [False] * len(joueurs)
        self.updated = False

    def update(self):
        self.updated = True


def test_init_ok():
    j = Joueur("Alice", [], 100, 42)
    assert j.nom == "Alice"
    assert j.jetons_restants == 100
    assert j.id_compte == 42
    assert j.mise == 0


def test_init_nom_invalide():
    with pytest.raises(TypeError):
        Joueur(123, [], 100)


def test_init_jetons_invalides():
    with pytest.raises(TypeError):
        Joueur("Bob", [], "100")


def test_str():
    j = Joueur("Charlie", [], 50)
    assert str(j) == "Charlie avec 50"


def test_small_blind():
    j = Joueur("A", [], 100)
    m = FakeManche([j])
    j.small_blind(20, m)
    assert j.jetons_restants == 80
    assert j.mise == 20
    assert m.pot == 20


def test_small_blind_insuffisant(capsys):
    j = Joueur("A", [], 5)
    m = FakeManche([j])
    j.small_blind(20, m)
    out = capsys.readouterr().out
    assert "Pas assez de jetons" in out


def test_big_blind():
    j = Joueur("B", [], 100)
    m = FakeManche([j])
    j.big_blind(30, m)
    assert j.jetons_restants == 70
    assert j.mise == 30
    assert m.pot == 30


def test_big_blind_insuffisant(capsys):
    j = Joueur("B", [], 5)
    m = FakeManche([j])
    j.big_blind(30, m)
    out = capsys.readouterr().out
    assert "Pas assez de jetons" in out


def test_relancer_pas_ton_tour(capsys):
    j1 = Joueur("A", [], 100)
    j2 = Joueur("B", [], 100)
    m = FakeManche([j1, j2])
    m.tour = 1
    j1.relancer(20, m)
    out = capsys.readouterr().out
    assert "Pas à ton tour" in out


def test_relancer_ok():
    j1 = Joueur("A", [], 100)
    m = FakeManche([j1])
    j1.relancer(20, m)
    assert j1.jetons_restants == 80
    assert m.pot == 20
    assert m.updated


def test_relancer_insuffisant(capsys):
    j1 = Joueur("A", [], 10)
    m = FakeManche([j1])
    j1.relancer(50, m)
    out = capsys.readouterr().out
    assert "Pas assez de jetons" in out


def test_relancer_inferieur_mise(capsys):
    j1 = Joueur("A", [], 100)
    m = FakeManche([j1])
    j1.relancer(5, m)
    out = capsys.readouterr().out
    assert "relance inférieure" in out


def test_suivre_ok():
    j = Joueur("A", [], 100)
    m = FakeManche([j], mise=20)
    j.suivre(m)
    assert j.jetons_restants == 80
    assert m.pot == 20
    assert m.updated


def test_suivre_pas_ton_tour(capsys):
    j1 = Joueur("A", [], 100)
    j2 = Joueur("B", [], 100)
    m = FakeManche([j1, j2], mise=20)
    m.tour = 1
    j1.suivre(m)
    out = capsys.readouterr().out
    assert "Pas à ton tour" in out


def test_suivre_insuffisant(capsys):
    j = Joueur("A", [], 10)
    m = FakeManche([j], mise=50)
    j.suivre(m)
    out = capsys.readouterr().out
    assert "Pas assez de jetons" in out


def test_couche_ok():
    j1 = Joueur("A", [], 100)
    m = FakeManche([j1])
    j1.couche(m)
    assert m.couche[0]
    assert m.updated


def test_couche_pas_ton_tour(capsys):
    j1 = Joueur("A", [], 100)
    j2 = Joueur("B", [], 100)
    m = FakeManche([j1, j2])
    m.tour = 1
    j1.couche(m)
    out = capsys.readouterr().out
    assert "Pas à ton tour" in out