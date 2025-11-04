class Admin():
    def __init__(self, nom, mdp):
        self.nom = nom
        self.mdp = mdp

    def crediter_compte(self, compte, nbj):
        compte.nb_jetons += nbj
        