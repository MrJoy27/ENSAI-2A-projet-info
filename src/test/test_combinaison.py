import unittest

class TestCombinaison(unittest.TestCase):

    def test_quinte_flush_royale(self):
        main = ListeCartes([
            Carte("Dix", "Cœur"),
            Carte("Valet", "Cœur"),
            Carte("Dame", "Cœur"),
            Carte("Roi", "Cœur"),
            Carte("As", "Cœur")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Quinte Flush Royale")

    def test_quinte_flush(self):
        main = ListeCartes([
            Carte("Six", "Pique"),
            Carte("Sept", "Pique"),
            Carte("Huit", "Pique"),
            Carte("Neuf", "Pique"),
            Carte("Dix", "Pique")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Quinte Flush")

    def test_carre(self):
        main = ListeCartes([
            Carte("As", "Trèfle"),
            Carte("As", "Cœur"),
            Carte("As", "Pique"),
            Carte("As", "Carreau"),
            Carte("Roi", "Cœur")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Carré")

    def test_full(self):
        main = ListeCartes([
            Carte("Dame", "Trèfle"),
            Carte("Dame", "Cœur"),
            Carte("Dame", "Carreau"),
            Carte("Neuf", "Trèfle"),
            Carte("Neuf", "Cœur")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Full")

    def test_couleur(self):
        main = ListeCartes([
            Carte("Deux", "Carreau"),
            Carte("Cinq", "Carreau"),
            Carte("Neuf", "Carreau"),
            Carte("Valet", "Carreau"),
            Carte("Roi", "Carreau")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Couleur")

    def test_quinte(self):
        main = ListeCartes([
            Carte("Cinq", "Trèfle"),
            Carte("Six", "Cœur"),
            Carte("Sept", "Carreau"),
            Carte("Huit", "Pique"),
            Carte("Neuf", "Trèfle")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Quinte")

    def test_brelan(self):
        main = ListeCartes([
            Carte("Valet", "Carreau"),
            Carte("Valet", "Trèfle"),
            Carte("Valet", "Cœur"),
            Carte("Trois", "Carreau"),
            Carte("Sept", "Pique")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Brelan")

    def test_double_paire(self):
        main = ListeCartes([
            Carte("Dix", "Carreau"),
            Carte("Dix", "Trèfle"),
            Carte("Roi", "Cœur"),
            Carte("Roi", "Pique"),
            Carte("Deux", "Cœur")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Double Paire")

    def test_paire(self):
        main = ListeCartes([
            Carte("Six", "Carreau"),
            Carte("Six", "Trèfle"),
            Carte("Dix", "Cœur"),
            Carte("Valet", "Pique"),
            Carte("Roi", "Cœur")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Paire")

    def test_hauteur(self):
        main = ListeCartes([
            Carte("Deux", "Carreau"),
            Carte("Cinq", "Trèfle"),
            Carte("Sept", "Cœur"),
            Carte("Valet", "Pique"),
            Carte("Roi", "Cœur")
        ])
        combinaison = Combinaison(main)
        self.assertEqual(combinaison.type, "Hauteur")