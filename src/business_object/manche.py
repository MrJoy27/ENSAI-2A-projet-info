from random import randint
from itertools import combinations
from business_object.combinaison import Combinaison
from dao.admin_dao import adminDao

class Manche():
    def __init__(self, liste_joueurs, riviere, small_blind, big_blind):
        if not small_blind*2 <= big_blind:
            raise ValueError(
                "La big blind doit être au moins deux fois supérieure à la small blind"
                )
        self.liste_joueurs = liste_joueurs
        self.pot = 0
        self.mise = big_blind
        self.riviere = riviere
        self.revele = [False for _ in range(5)]
        self.couche = [False for _ in range(len(liste_joueurs))]
        self.dealer = randint(0, len(self.liste_joueurs)-1)
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.n=len(self.liste_joueurs)
        self.tour=self.dealer+1
        self.t1=True
        self.win=""

    def blindes(self):
        j_small_blind = self.liste_joueurs[(self.dealer+1)%self.n]
        j_big_blind = self.liste_joueurs[(self.dealer+2)%self.n]
        j_small_blind.small_blind(self.small_blind, self)
        j_big_blind.big_blind(self.big_blind, self)
        self.tour+=2

    def finir_manche(self):
        non_couche=[]
        for i in range(len(self.couche)): 
            if not self.couche[i]:
                non_couche.append(self.liste_joueurs[i])
        meilleures_combinaisons=[]
        jc = []
        for joueur in non_couche:
            cartes=joueur.main+self.riviere
            combinaisons=[]
            possibilites=combinations(cartes, 5)
            for possibilite in possibilites:
                combinaisons.append(Combinaison(possibilite))
            bc = max(combinaisons)
            meilleures_combinaisons.append(bc)
            jc.append([bc, joueur])
        best=max(meilleures_combinaisons)
        joueurs_gagnants=[]
        for bi in jc:
            if bi[0] == best:
                joueurs_gagnants.append(bi[1])
        ad=adminDao()
        for joueur in self.liste_joueurs:
            ad.modifier_jetons(joueur.nom,joueur.jetons_restants)
        if len(joueurs_gagnants) == 1:
            ad.crediter(joueurs_gagnants[0].nom, self.pot)
            
        if len(joueurs_gagnants) >= 2:
            gain = self.pot/len(joueurs_gagnants)
            for joueur in joueurs_gagnants:
                ad.crediter(joueur, gain)
        
        self.liste_joueurs = []
        self.win = f"Manche remportée par {joueurs_gagnants[0].nom}"
        if len(joueurs_gagnants) >= 2:
            for i in range(1, len(joueurs_gagnants)):
                self.win += f" et {joueurs_gagnants[i]}"
        
        

    def update(self):
        if self.couche.count(False)>1 and self.revele.count(False)>0:
            if self.t1 and self.tour%self.n==((self.dealer+2)%self.n):
                self.t1=False
            if not self.t1:
                c = 0
                for joueur in self.liste_joueurs:
                    if joueur.mise == self.mise:
                        c += 1
                if c == self.couche.count(False):
                    if self.revele.count(False) == 5:
                        self.revele[0] = True
                        self.revele[1] = True
                        self.revele[2] = True
                        self.mise = 0
                        self.tour -= 1
                    elif self.revele.count(False) == 2:
                        self.revele[3] = True
                        self.mise = 0
                        self.tour -= 1
                    else:
                        self.revele[4] = True
            j=1
            while self.couche[(self.tour+j)%self.n]:
                j+=1
            self.tour+=j
        else:
            self.finir_manche()

    def voir_riviere(self):
        rev = []
        for i in range(5):
            if self.revele[i]:
                rev.append(self.riviere[i])
        return rev

    