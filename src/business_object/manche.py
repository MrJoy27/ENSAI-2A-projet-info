from random import randint

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
        self.tour_joue = False
        self.dealer = randint(0, len(self.liste_joueurs)-1)
        self.small_blind = small_blind
        self.big_blind = big_blind

    def voir_riviere(self):
        rev = []
        for i in range(5):
            if self.revele[i]:
                rev.append(self.riviere[i])
        return rev

    def finir_manche(self):
        n = len(self.liste_joueurs)
        t1 = True
        j_small_blind = self.liste_joueurs[(self.dealer+1)%n]
        j_big_blind = self.liste_joueurs[(small_blind+1)%n]
        tour = (j_big_blind+1)%n
        j_small_blind.small_blind(self.small_blind, self)
        j_big_blind.big_blind(self.big_blind, self)
        while self.couche.count(False) > 1 or self.revele.count(False) > 0:
            while not self.tour_joue:
                joueur = self.liste_joueurs[tour%n]
                if t1 and joueur == j_big_blind:
                    t1 = False
            if not t1:
                c = 0
                for joueur in self.liste_joueurs:
                    if joueur.mise == self.mise:
                        c += 1
                if c == self.couche.count(False):
                    if self.revele.count(False) == 5:
                        self.revele[0] = True
                        self.revele[1] = True
                        self.revele[2] = True
                    if self.revele.count(False) == 2:
                        self.revele[3] = True
                    else:
                        self.revele[4] = True
            self.tour_joue = False
            tour += 1
        
            