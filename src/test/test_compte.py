import pytest
from business_object.compte import Compte

# Table factice pour les tests
class Table:
    def __init__(self):
        self.liste_comptes = []

def test_initialisation():
    compte = Compte("Alice", "secret", 100, 5, 10, id=42)
    assert compte.nom == "Alice"
    assert compte.mdp == "secret"
    assert compte.nb_jetons == 100
    assert compte.nb_victoires == 5
    assert compte.nb_parties == 10
    assert compte.id == 42

def test_rejoindre_table():
    table = Table()
    compte = Compte("Bob")
    compte.rejoindre_table(table)
    assert compte in table.liste_comptes

def test_rejoindre_table_limite():
    table = Table()
    for i in range(10):
        table.liste_comptes.append(Compte(f"Joueur{i}"))
    compte = Compte("Trop")
    compte.rejoindre_table(table)
    assert compte not in table.liste_comptes  # ne doit pas être ajouté

def test_quitter_table():
    table = Table()
    compte = Compte("Charlie")
    table.liste_comptes.append(compte)
    compte.quitter_table(table)
    assert compte not in table.liste_comptes

def test_quitter_table_non_present(capsys):
    table = Table()
    compte = Compte("Delta")
    compte.quitter_table(table)
    captured = capsys.readouterr()
    assert "Joueur pas sur cette table" in captured.out

def test_view_profile(capsys):
    compte = Compte("Echo", nb_jetons=50, nb_victoires=3, nb_parties=7)
    compte.view_profile()
    captured = capsys.readouterr()
    assert "Nombre de jetons : 50" in captured.out
    assert "Nombre de victoires : 3" in captured.out
    assert "Nombre de parties jouées : 7" in captured.out
