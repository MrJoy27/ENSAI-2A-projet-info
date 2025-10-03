from src.business_object.carte.deck import Deck
from src.businees_object.manche import Manche
from scrc.business_object.joueur import Joueur

class Table():
    def __init__(self):
        self.liste_comptes = []
        self.deck = Deck()
    
    def commencer_manche(self):
        if len(self.liste_comptes) < 2:
            print("Pas assez de joueurs")
        else:
            self.deck.melanger()
            liste_joueurs = []
            for acc in self.liste_comptes:
                joueur = Joueur(acc.nom, [], acc.nb_jetons, acc.id)
                liste_joueurs.append(joueur)
            for _ in range(2):
                for joueur in liste_joueurs:
                    joueur.main.append(piocher(self.deck))
            riviere = []
            for _ in range(5):
                riviere.append(piocher(self.deck))
            manche = Manche(liste_joueurs, riviere)
            return manche
