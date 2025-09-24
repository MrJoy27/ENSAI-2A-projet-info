
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
    class Joueur {
      +nom: str
      +main: list(Carte)
      +jetons_restants: int
      +id_compte: int //
      +relancer()
      +suivre()
      +se_coucher()
      +jetons_restants()
    }
    
    class Carte {
      +Valeur: Valeur(enum)
      +Couleur: Couleur(enum)
    }
    
    class Manche {
      +liste_joueurs:list(Joueur)
      +pot:int
      +riviere:list(Carte)
      +revele:list(Bool)
      +couche:list(Bool)//
      +finir_manche()
    }

    class Table {
      +liste_compte: list(Compte)
      +deck: deck //
      +commencer_manche()
    }
    
    class Compte {
      +id: int
      +nom: str
      +mdp: str
      +nb_jetons: int
      +nb_parties_gagnées: int //
      +rejoindre_table(table)
      +quitter_table(table)
      +se_connecter()
      +se_deconnecter()
      +voir_profil()
    }

    class Admin {
      +mdp:int//
      +accrediter_jetons(Joueur)
    }

    class Deck {
      +liste_carte: list(Carte)//
      +melanger()
      +piocher(): Carte
    }

    Carte -- Joueur
    Carte -- Manche
    Carte -- Deck
    Deck -- Table
    Joueur -- Compte
    Joueur -- Manche
    Manche -- Table
    Table -- Compte
    Compte -- Admin
```
