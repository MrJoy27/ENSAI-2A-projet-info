from business_object.carte.deck import Deck
from business_object.manche import Manche
from business_object.joueur import Joueur

class Table():
    def __init__(self, id):
        self.liste_comptes = []
        self.deck = Deck()
        self.id = id
        self.manche = None
    
    def commencer_manche(self, small, big):
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
                    joueur.main.append(self.deck.piocher())
            riviere = []
            for _ in range(5):
                riviere.append(self.deck.piocher())
            manche = Manche(liste_joueurs, riviere, small, big)
            manche.blindes()
            self.manche = manche
            return manche
