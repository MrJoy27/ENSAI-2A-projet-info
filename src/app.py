import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from business_object.table import Table

from service.joueur_service import compteService
from service.admin_service import adminService
from utils.log_init import initialiser_logs

app = FastAPI(title="Mon webservice")


initialiser_logs("Webservice")
tables = []
joueur_service = compteService()
aservice = adminService()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


@app.get("/admin/", tags=["Admin"])
async def lister_tous_joueurs(mdp):
    """Lister tous les joueurs"""
    if mdp != "crab_love":
        raise HTTPException(status_code=401, detail="Mot de passe administrateur erroné")
    logging.info("Lister tous les joueurs")
    liste_joueurs = aservice.lister_tous()

    liste_model = []
    for joueur in liste_joueurs:
        liste_model.append(joueur)

    return liste_model


@app.get("/admin/{nom_joueur}", tags=["Admin"])
async def joueur_par_nom(mdp, nom_joueur):
    """Trouver un joueur à partir de son id"""
    if mdp != "crab_love":
        raise HTTPException(status_code=401, detail="Mot de passe administrateur erroné")
    logging.info("Trouver un joueur à partir de son id")
    return aservice.trouver_par_nom(nom_joueur)


@app.put("/admin/{nom_joueur}", tags=["Admin"])
def crediter_joueur(mdp, nom_joueur, nb_jetons):
    """Modifier un joueur"""
    if mdp != "crab_love":
        raise HTTPException(status_code=401, detail="Mot de passe administrateur erroné")
    logging.info("Modifier un joueur")
    joueur = aservice.trouver_par_nom(nom_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    succes = aservice.crediter(nom_joueur, nb_jetons)
    if not succes:
        raise HTTPException(status_code=404, detail="Erreur lors du crédit du joueur")

    return f"Joueur {nom_joueur} crédité de {nb_jetons}"


@app.delete("/admin/{nom_joueur}", tags=["Admin"])
def supprimer_joueur(mdp, nom_joueur):
    """Supprimer un joueur"""
    if mdp != "crab_love":
        raise HTTPException(status_code=401, detail="Mot de passe administrateur erroné")
    logging.info("Supprimer un joueur")
    joueur = aservice.trouver_par_nom(nom_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    aservice.supprimer(nom_joueur)
    return f"Joueur {nom_joueur} supprimé"

class JoueurModel(BaseModel):
    """Définir un modèle Pydantic pour les Joueurs"""

    nom: str
    mdp: str

@app.post("/joueur/", tags=["Joueurs"])
async def creer_joueur(j: JoueurModel):
    """Créer un joueur"""
    logging.info("Créer un joueur")
    if adminService().pseudo_deja_utilise(j.nom):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")

    joueur = joueur_service.creer(j.nom, j.mdp)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la création du joueur")

    return joueur

@app.post("/table/", tags=["Tables"])
def creer_table():
    tables.append(Table(len(tables)+1))
    return tables

@app.put("/table/{table_id}", tags=["Tables"])
def rejoindre_table(nom, mdp, id_table: int):
    compte = adminService().trouver_par_nom(nom)
    if not compte:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    if not compte.mdp == mdp:
        raise HTTPException(status_code=401, detail="Mot de passe erroné")
    table = None
    for tab in tables:
        if tab.id == id_table:
            table = tab
    if table is not None:
        if len(table.list_comptes) < 10:
            table.liste_comptes.append(compte)
            return table.liste_comptes
        else:
            raise HTTPException(status_code=405, detail="Plus de place à la table")
    else:
        raise HTTPException(status_code=404, detail="Table non trouvée")

@app.get("/table/{table_id}", tags=["Tables"])
def etat_table(id: int):
    table = None
    for tab in tables:
        if tab.id == id:
            table = tab
    if table is not None:
        return table.liste_comptes
    else:
        raise HTTPException(status_code=404, detail="Table non trouvée")

@app.post("/manche/", tags=["Manche"])
def lancer_manche(id_table: int):
    pass

@app.get("/manche/{table_id}", tags=["Manche"])
def etat_manche():
    pass




# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
