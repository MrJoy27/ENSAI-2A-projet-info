from src.business_object.carte.liste_cartes import ListeCartes

class Joueur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    nom:str
    main:liste[Carte]
    jetons_restants:int
    id_compte:int

    """

    def __init__(self, nom, main, jetons_restants, id_compte):
        """Constructeur"""
        if not(isinstance(nom, str)):
            raise TypeError("nom doit etre de type str")
        if not(isinstance(main, ListeCartes)):
            raise TypeError("main doit etre de type ListeCartes")
        if not(isinstance(jetons_restants, int)):
            raise TypeError("jetons_restants doit etre de type int")
        if not(isinstance(jetons_restants, int)):
            raise TypeError("id_compte doit etre de type int")
        self.nom= nom
        self.main=main
        self.jetons_restants=jetons_restants
        self.id_compte=id_compte

    def __str__(self):
        """Permet d'afficher les informations du joueur sans ses cartes qui restent cachés"""
        return f"{self.nom} avec {self.jetons_restants}"

    def voir_main(self):
        print(self.main)

    def voir_jetons_restants(self):
        print(self.jetons_restants)
    
    def relancer(self, nb_jetons, manche):
        if nb_jetons > self.jetons_restants:
            print("Pas assez de jetons")
        elif nb_jetons < manche.mise:
            print("relance inférieure à la mise minimale")
        else:
            manche.mise = nb_jetons
            manche.pot += nb_jetons
            self.jetons_restants -= nb_jetons
            manche.tour_joue = True

    def suivre(self, manche):
        if self.jetons_restants >= manche.mise:
            self.jetons_restants -= manche.mise
            manche.pot += manche.mise
            manche.tour_joue = True
        else:
            print("Pas assez de jetons")

    def couche(self, manche):
        pos = 0
        for i in range(len(manche.joueurs)):
            if manche.joueurs[i] == self:
                pos = i
        manche.couche[i] = True
        manche.tour_joue = True
