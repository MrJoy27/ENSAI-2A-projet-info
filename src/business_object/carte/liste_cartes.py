"""Implémentation de la classe _ListeCartes."""

from src.business_object.carte.carte import Carte
import copy
import random


class ListeCartes:

    """
     une liste de cartes
    """

    def __init__(self, cartes: list[Carte]):
        if not isinstance(cartes, list):
            raise ValueError("L'argument 'cartes' doit être "
                             "None ou une liste de cartes.")
        else:
            for card in cartes:
                if not isinstance(card, Carte):
                    raise ValueError("L'argument 'cartes' doit être "
                                     "None ou une liste de cartes.")
        self.__cartes = cartes

    @property
    def cartes(self):
        return copy.deepcopy(self.__cartes)

    def __eq__(self, liste_cartes):
        if not isinstance(liste_cartes, _ListeCartes):
            return False
        else:
            for card in self.__cartes:
                if card not in liste_cartes.__cartes:
                    return False
            return len(self.__cartes) == len(liste_cartes.__cartes)

    def __str__(self):
        if self.__cartes == []:
            return "[]"
        combi_str = "["+str(self.__cartes[0])
        for card in self.__cartes[1:]:
            combi_str += ", "
            combi_str += str(card)
        return combi_str+"]"

    def __len__(self):
        return len(self.__cartes)

    def melanger(self):
        """
        melanger mélange la liste de cartes

        """
        random.shuffle(self.__cartes)

    def ajouter_carte(self, card):
        """
        ajouter_carte ajoute une carte à la liste de cartes

        Parameters
        ----------
        card : Carte
            une carte

        Raises
        ------
        TypeError
            si l'argument card n'est pas une carte
        """
        if not isinstance(card, Carte):
            raise TypeError("L'argument 'carte' doit être une instance de Carte.")
        self.__cartes.append(card)

    def retirer_carte(self, indice):
        """
        retirer_carte retire la carte d'indice indice de la liste de carte

        Parameters
        ----------
        indice : int
            l'indice de la carte à retirer de la liste

        Returns
        -------
        Carte
            la carte retirée de la liste

        Raises
        ------
        Exception
            si la liste est vide, on ne peut rien retirer
        ValueError
            si l'indice n'est pas un entier, on ne peut rien retirer
        ValueError
            si l'indice est un entier hors des limites de la liste,
            on ne peut rien retirer
        """
        if self.__cartes == []:
            raise Exception("La liste de cartes est vide, "
                            "aucune carte ne peut être retirée.")
        if not isinstance(indice, int):
            raise ValueError("L'indice de la carte à retirer n'est pas valide. "
                             "L'indice doit être un entier compris entre "
                             f"0 et {len(self.__cartes)-1} inclus, "
                             f"mais l'indice est '{indice}'.")
        elif indice < 0 or indice > len(self.__cartes)-1:
            raise ValueError("L'indice de la carte à retirer n'est pas valide. "
                             "L'indice doit être un entier compris entre "
                             f"0 et {len(self.__cartes)-1} inclus, "
                             f"mais l'indice est {indice}.")
        return self.__cartes.pop(int(indice))
    def max(self):
        return max(self.__cartes)