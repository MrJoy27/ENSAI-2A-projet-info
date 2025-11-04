from src.business_object.carte.liste_cartes import ListeCartes

class Combinaison():
    def __init__(self, liste_cartes):
        if not isinstance(liste_cartes,ListeCartes):
            raise TypeError("liste_cartes doit etre de type liste_cartes")
        if len(liste_cartes)!=5:
            raise ValueError("liste_cartes doit etre de taille 5")
        self.liste_cartes==liste_cartes
        #Quinte flush royale
        flush_royale=["10","Valet","Dame","Roi","As"]
        flush_royale_verif=[False in range(5)]
        couleur=liste_cartes[0].couleur
        ordre=["As","2","3","4","5","6","7","8","9","10","Valet","Dame","Roi"]
        ordre_verif=[False in range(13)]
        est_couleur=True
        cpt_carte=[0 for i in range(13)]

        for carte in self.liste_cartes:
            if couleur!=carte.couleur:
                est_couleur=False
            ordre_verif[ordre.index(carte.valeur)]=True
        if ordre_verif.count("True")==5:
            if ordre_verif[12]==True and ordre_verif[11]==True and ordre_verif[10]==True and ordre_verif[9]==True ordre_verif[0]==True:
                self.type="Flush Royale"
            elif:
                for i in range(ordre_verif-5):
                    if ordre_verif[val]==True:
                        if ordre_verif[val+1] and ordre_verif[val+2] and ordre_verif[val+3] and ordre_verif[val+4]:
                            est_quinte=True
            else:
                cpt_carte=[0 for i in range(13)]
                for carte in self.liste_cartes:
                    cpt_carte[ordre.index(carte.valeur)]+=1
                brelan=False
                paire1=False
                paire2=False
                for i in range(13):
                    if cpt_carte==4:
                        self.type="Carré"
                        break
                    elif cpt_carte==3:
                        brelan=True
                    elif cpt_carte==2 and not(paire1):
                        paire1=True
                    else:
                        if cpt_carte==2:
                            paire2=True
                if brelan and paire1:
                    self.type="Full"
                else: 
                    if est_couleur:
                        self.type="Couleur"
                
        
                