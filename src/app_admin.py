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
aservice = adminService()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


@app.get("/joueur/", tags=["Joueurs"])
async def lister_tous_joueurs():
    """Lister tous les joueurs"""
    logging.info("Lister tous les joueurs")
    liste_joueurs = aservice.lister_tous()

    liste_model = []
    for joueur in liste_joueurs:
        liste_model.append(joueur)

    return liste_model


@app.get("/joueur/{nom_joueur}", tags=["Joueurs"])
async def joueur_par_nom(nom_joueur):
    """Trouver un joueur à partir de son id"""
    logging.info("Trouver un joueur à partir de son id")
    return aservice.trouver_par_nom(nom_joueur)


@app.put("/joueur/{nom_joueur}", tags=["Joueurs"])
def crediter_joueur(nom_joueur, nb_jetons):
    """Modifier un joueur"""
    logging.info("Modifier un joueur")
    joueur = aservice.trouver_par_nom(nom_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    succes = aservice.crediter(nom_joueur, nb_jetons)
    if not succes:
        raise HTTPException(status_code=404, detail="Erreur lors du crédit du joueur")

    return f"Joueur {nom_joueur} crédité de {nb_jetons}"


@app.delete("/joueur/{nom_joueur}", tags=["Joueurs"])
def supprimer_joueur(nom_joueur):
    """Supprimer un joueur"""
    logging.info("Supprimer un joueur")
    joueur = aservice.trouver_par_nom(nom_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    aservice.supprimer(nom_joueur)
    return f"Joueur {nom_joueur} supprimé"


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
