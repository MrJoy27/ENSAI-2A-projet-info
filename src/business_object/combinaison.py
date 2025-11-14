from business_object.carte.liste_cartes import ListeCartes
from business_object.carte.carte import Carte, Valeur, Couleur

class Combinaison():
    def __init__(self, liste_cartes):
        #if not isinstance(liste_cartes,ListeCartes):
            #raise TypeError("liste_cartes doit etre de type liste_cartes")
        if len(liste_cartes)!=5:
            raise ValueError("liste_cartes doit etre de taille 5")
        self.liste_cartes=liste_cartes
        #Quinte flush royale
        couleur=liste_cartes[0].couleur
        ordre=["As","Deux","Trois","Quatre","Cinq","Six","Sept","Huit","Neuf","Dix","Valet","Dame","Roi"]
        ordre_valeur=[Valeur.As,Valeur.Deux,Valeur.Trois,Valeur.Quatre,Valeur.Cinq,Valeur.Six,Valeur.Sept,Valeur.Huit,Valeur.Neuf,Valeur.Dix,Valeur.Valet,Valeur.Dame,Valeur.Roi]
        est_couleur=True
        est_quinte=False
        brelan=False
        paire1=False
        paire2=False
        carre=False
        cpt_carte=[0 for i in range(13)]
        #creation de cpt_cartes et de est_couleur
        for carte in liste_cartes:
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
                if cpt_carte[i]==2:
                    paire2=True
        if cpt_carte[9]==1 and cpt_carte[10]==1 and cpt_carte[11]==1 and cpt_carte[12]==1 and cpt_carte[0]==1 and est_couleur:
            self.type="Quinte Flush Royale"
            self.tie_breaker=[max(liste_cartes)] 
        elif est_quinte and est_couleur:
            self.type="Quinte Flush"
            self.tie_breaker=[max(liste_cartes)]
        elif carre:
            self.type="Carré"
            self.tie_breaker=[Carte(ordre_valeur[cpt_carte.index(4)], Couleur.Carreau)]
        elif est_couleur:
            self.type="Couleur"
            self.tie_breaker=[max(liste_cartes)]
        elif brelan and paire1:
            self.type="Full"
            self.tie_breaker=[Carte(ordre_valeur[cpt_carte.index(3)],Couleur.Carreau), Carte(ordre_valeur[cpt_carte.index(2)],Couleur.Carreau)]
        elif est_quinte:
            self.type="Quinte"
            self.tie_breaker=[max(liste_cartes)]
        elif brelan:
            self.type="Brelan"
            self.tie_breaker=[Carte(ordre_valeur[cpt_carte.index(3)],Couleur.Carreau)]
        elif paire1 and paire2:
            self.type="Double Paire"
            self.tie_breaker=[Carte(ordre_valeur[cpt_carte.index(2)],Couleur.Carreau)]
            cpt_carte.pop(cpt_carte.index(2))
            self.tie_breaker.append([Carte(ordre_valeur[cpt_carte.index(2)],Couleur.Carreau)])
            # self.tie_breaker.sort(reverse=True)
        elif paire1:
            self.type="Paire"
            self.tie_breaker=[Carte(ordre_valeur[cpt_carte.index(2)],Couleur.Carreau)]
        else:
            self.type="Hauteur"
            self.tie_breaker=[max(liste_cartes)] 
    def __eq__(self,other):
        if self.type==other.type:
            for i in range(len(self.tie_breaker)):
                if self.tie_breaker[i]==other.tie_breaker[i]:
                    pass
                else:
                    return False
            return True
        else: 
            return False
    def __ne__(self,other):
        return not(self==other)      
    def __lt__(self,other):
        combinaisons_poker=[
        "Hauteur",
        "Paire",
        "Double Paire",
        "Brelan",
        "Quinte",
        "Couleur",
        "Full",
        "Carré",
        "Quinte Flush",
        "Quinte Flush Royale"
        ]
        if combinaisons_poker.index(self.type)<combinaisons_poker.index(other.type):
            return True
        elif self==other:
            return False
        elif combinaisons_poker.index(self.type)==combinaisons_poker.index(other.type):
            for i in range(len(self.tie_breaker)):
                if self.tie_breaker[i]<other.tie_breaker[i]:
                    return True
                elif self.tie_breaker[i]>other.tie_breaker[i]:
                    return False
        else:
            return False
    
    def __le__(self,other):
        combinaisons_poker=[
            "Hauteur",
            "Paire",
            "Double Paire",
            "Brelan",
            "Quinte",
            "Couleur",
            "Full",
            "Carré",
            "Quinte Flush",
            "Quinte Flush Royale"
            ]
        if combinaisons_poker.index(self.type)<combinaisons_poker.index(other.type):
            return True
        elif self==other:
            return True
        elif combinaisons_poker.index(self.type)==combinaisons_poker.index(other.type):
            for i in range(len(self.tie_breaker)):
                if self.tie_breaker[i]<other.tie_breaker[i]:
                    return True
                elif self.tie_breaker[i]>other.tie_breaker[i]:
                    return False
        else:
            return False
            
    def __ge__(self,other):
        return not(self<other)
    def __gt__(self,other):
        return not(self <=other)
    
    
                