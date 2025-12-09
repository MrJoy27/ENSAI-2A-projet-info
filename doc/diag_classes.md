
# Diagramme de classes des objets métiers

Ce diagramme est codé avec [mermaid](https://mermaid.js.org/syntax/classDiagram.html) :

* avantage : facile à coder
* inconvénient : on ne maîtrise pas bien l'affichage

Pour afficher ce diagramme dans VScode :

* à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
* rechercher `mermaid`
  * installer l'extension **Markdown Preview Mermaid Support**
* revenir sur ce fichier
  * faire **CTRL + K**, puis **V**v

```mermaid

classDiagram
    directionLR
    class Joueur {
      +nom: str
      +main: ListeCartes
      +jetons_restants: int
      +id_compte: int
      +mise: int

      +__init__(nom, main, jetons_restants, id_compte=None, mise=0)
      +__str__(): str
      +voir_main()
      +voir_jetons_restants()
      +small_blind(nb, manche)
      +big_blind(nb, manche)
      +relancer(nb_jetons, manche)
      +suivre(manche)
      +couche(manche)
    }

    class Carte{
      +couleur: Couleur[enum]
      +valeur: Valeur[enum]
    }
    
    
    class Manche {
      +liste_joueurs: list[Joueur]
      +pot: int
      +mise: int
      +riviere: list[Carte]
      +revele: list[bool]
      +couche: list[bool]
      +dealer: int
      +small_blind: int
      +big_blind: int
      +n: int
      +tour: int
      +t1: bool
      +win: str

      +__init__(liste_joueurs, riviere, small_blind, big_blind)
      +blindes()
      +finir_manche()
      +update()
      +voir_riviere(): list[Carte]
    }


    class Table {
      +liste_comptes: list[Compte]
      +deck: Deck
      +id: int
      +manche: Manche

      +__init__(id)
      +commencer_manche(small, big): Manche
    }

    
    class Compte {
      +id: int
      +nom: str
      +mdp: str
      +nb_jetons: int
      +nb_victoires: int
      +nb_parties: int

      +__init__(nom, mdp=None, nb_jetons=0, nb_victoires=0, nb_parties=0, id=None)
      +as_list(): list[str]
      +rejoindre_table(table)
      +quitter_table(table)
      +view_profile()
    }

    class ListeCartes {
      -__cartes: list[Carte]

      +__init__(cartes: list[Carte])
      +cartes(): list[Carte]
      +__eq__(liste_cartes): bool
      +__str__(): str
      +__len__(): int
      +melanger()
      +ajouter_carte(card: Carte)
      +retirer_carte(indice: int): Carte
      +max(): Carte
    }


    class Combinaison {
      +liste_cartes : ListeCartes
      +type : str
      +tie_breaker : list

      +__init__(liste_cartes)
      +__eq__(other) : bool
      +__ne__(other) : bool
      +__lt__(other) : bool
      +__le__(other) : bool
      +__gt__(other) : bool
      +__ge__(other) : bool
  }

    class Deck {
      +liste_carte: list[Carte]
      +melanger()
      +piocher(): Carte
    }

    Carte -- Joueur
    Carte -- Manche
    Carte -- ListeCartes
    ListeCartes -- Deck
    Deck -- Table
    Joueur -- Compte
    Joueur -- Manche
    Manche -- Combinaison
    Combinaison -- Carte
    Manche -- Table
    Table -- Compte
```
