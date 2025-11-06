import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from service.joueur_service import compteService
from service.admin_service import adminService
from utils.log_init import initialiser_logs

app = FastAPI(title="Mon webservice")


initialiser_logs("Webservice")

joueur_service = compteService()

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")

@app.post("/joueur/", tags=["Joueurs"])
async def creer_joueur(j: JoueurModel):
    """Créer un joueur"""
    logging.info("Créer un joueur")
    if aservice.pseudo_deja_utilise(j.nom):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")

    joueur = joueur_service.creer(j.nom, j.mdp)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la création du joueur")

    return joueur
