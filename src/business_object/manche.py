class Manche():
    def __init__(self, liste_joueurs, riviere):
        self.liste_joueurs = liste_joueurs
        self.pot = 0
        self.riviere = riviere
        self.revele = [False for _ in range(5)]
        self.couche = [False for _ in range(len(liste_joueurs))]
        self.tour_joue = False

    def voir_riviere(self):
        rev = []
        for i in range(5):
            if self.revele[i]:
                rev.append(self.riviere[i])
        return rev

    def finir_manche(self):
        ct = 0
        mod = 0
        while self.couche.count(False) > 1 or self.revele.count(False) > 0:
            if self.couche:
                ct += 1
            else:
                while not self.tour_joue:
                    pass
                self.tour_joue = False
                ct += 1
        
            