from src.business_object.carte.liste_cartes import ListeCartes

class Combinaison():
    def __init__(self, liste_cartes):
        if not isinstance(liste_cartes,ListeCartes):
            raise TypeError("liste_cartes doit etre de type liste_cartes")
        if len(liste_cartes)!=5:
            raise ValueError("liste_cartes doit etre de taille 5")
        self.liste_cartes=liste_cartes
        #Quinte flush royale
        couleur=liste_cartes[0].couleur
        ordre=["As","Deux","Trois","Quatre","Cinq","Six","Sept","Huit","Neuf","Dix","Valet","Dame","Roi"]
        est_couleur=True
        est_quinte=False
        brelan=False
        paire1=False
        paire2=False
        carre=False
        cpt_carte=[0 for i in range(13)]
        #creation de cpt_cartes et de est_couleur
        for carte in self.liste_cartes:
            if couleur!=carte.couleur:
                est_couleur=False
            cpt_carte[ordre.index(carte.valeur)]+=1
        #quinte
        for i in range(8):
            if cpt_carte[i]==1 and cpt_carte[i+1]==1 and cpt_carte[i+2]==1 and cpt_carte[i+3]==1 and cpt_carte[i+4]==1:
                est_quinte=True    
        #carre brelan et paire
        for i in range(13):
            if cpt_carte[i]==4:
                carre=True
                break
            elif cpt_carte[i]==3:
                brelan=True
            elif cpt_carte[i]==2 and not(paire1):
                paire1=True
            else:
                if cpt_carte==2:
                    paire2=True
        if est_quinte and est_couleur:
            if cpt_carte[9] and cpt_carte[10] and cpt_carte[11] and cpt_carte[12] and cpt_carte[0]:
                self.type="Quinte Flush Royale"
            else:
                self.type="Quinte Flush"
        elif carre:
            self.type="Carré"
        elif brelan and paire1:
            self.type="Full"
        elif est_quinte:
            self.type="Quinte"
        elif breland:
            self.type="Brelan"
        elif carte1 and carte2:
            self.type="Double Paire"
        elif paire:
            self.type="Paire"
        else:
            self.type="Hauteur"

            
        
                
        
                