class Compte():
    def __init__(self, id, nom, mdp):
        self.id = id
        self.nom = nom
        self.mdp = mdp
        self.nb_jetons = 0
        self.nb_victoires = 0
        self.nb_parties = 0

    def rejoindre_table(self, table):
        if len(table.joueurs) < 5:
            table.joueurs.append(self)
        else:
            print("Table remplie")
    
    def quitter_table(self, table):
        if self in table.joueurs:
            for i in range(len(table.joueurs)):
                if table.joueurs[i] == self:
                    table.joueurs.pop(i)
                    break
        else:
            print("Joueur pas sur cette table")
    
    def view_profile(self):
        print(f"Nombre de jetons : {self.nb_jetons}")
        print(f"Nombre de victoires : {self.nb_victoires}")
        print(f"Nombre de parties jouées : {self.nb_parties}")
