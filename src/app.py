import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from business_object.table import Table
from business_object.compte import Compte
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

@app.get("/admin/connexion", tags=["Admin"] )
async def connexion(mdp):
    if mdp != "crab_love":
        raise HTTPException(status_code=401, detail="Mot de passe administrateur erroné")
    else: 
        return True

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



@app.post("/joueur/", tags=["Joueurs"])
async def creer_joueur(pseudo, mdp):
    """Créer un joueur"""
    logging.info("Créer un joueur")
    if adminService().pseudo_deja_utilise(pseudo):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")

    joueur = joueur_service.creer(pseudo, mdp)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la création du joueur")

    return True


@app.post("/joueur/connexion", tags=["Joueurs"])
async def connexion_joueur(pseudo, mdp):
    """Se connecter"""
    logging.info("Se connecter")
    connexion = joueur_service.se_connecter(pseudo, mdp)
    if not connexion:
        raise HTTPException(status_code=404, detail="Problème de connexion")

    return True

@app.delete("/joueur/{pseudo}", tags=["Joueurs"])
def supprimer_compte(pseudo, mdp):
    """Supprimer un joueur"""
    logging.info("Supprimer un joueur")
    connexion = joueur_service.se_connecter(pseudo, mdp)
    if not connexion:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    aservice.supprimer(pseudo)
    return True

@app.get("/joueur/{pseudo}", tags=["Joueurs"])
def statistiques(pseudo):
    compte = joueur_service.stats(pseudo)
    if compte is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    return compte.nom, f"Nombre de victoires: {compte.nb_victoires}", f"Nombre de parties jouées: {compte.nb_parties}"


@app.post("/table/", tags=["Tables"])
def creer_table():
    id=len(tables)+1
    tables.append(Table(id))
    return id

@app.put("/table/{table_id}", tags=["Tables"])
def rejoindre_table(table_id: int,nom, mdp, ):
    compte = adminService().trouver_par_nom(nom)
    connexion=joueur_service.se_connecter(nom, mdp)
    if not connexion:
        raise HTTPException(status_code=401, detail="Mot de passe erroné")
    table = None
    for tab in tables:
        if tab.id == table_id:
            table = tab
    if table is not None:
        if len(table.liste_comptes) < 10:
            table.liste_comptes.append(Compte(nom=compte.nom, nb_jetons=compte.nb_jetons, nb_victoires=compte.nb_victoires, nb_parties=compte.nb_parties))
            return True
        else:
            raise HTTPException(status_code=405, detail="Plus de place à la table")
    else:
        raise HTTPException(status_code=404, detail="Table non trouvée")

@app.get("/table/{table_id}", tags=["Tables"])
def etat_table(table_id: int):
    table = None
    for tab in tables:
        if tab.id == table_id:
            table = tab
    if table is not None:
        return table.liste_comptes
    else:
        raise HTTPException(status_code=404, detail="Table non trouvée")

@app.delete("/table/{table_id}", tags=["Tables"])
def quitter_table(nom, mdp, table_id: int):
    compte = adminService().trouver_par_nom(nom)
    if not compte:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    if not compte.mdp == mdp:
        raise HTTPException(status_code=401, detail="Mot de passe erroné")
    table = None
    for tab in tables:
        if tab.id == table_id:
            table = tab
    if table is not None:
        for i in range(len(table.liste_comptes)):
            if table.liste_comptes[i].nom == compte.nom:
                table.liste_comptes.pop(i)
                return f"{compte.nom} a quitté la table"
        return "Joueur pas à la table"
    else:
        raise HTTPException(status_code=404, detail="Table non trouvée")

@app.post("/manche/", tags=["Manche"])
def lancer_manche(id_table: int, small: int, big: int):
    table = None
    for tab in tables:
        if tab.id == id_table:
            table = tab
    if table is not None:
        table.commencer_manche(small, big)
        return f'Début de la manche sur la table {table.id}'
    else:
        raise HTTPException(status_code=404, detail="Table non trouvée")

@app.get("/manche/{table_id}", tags=["Manche"])
async def etat_manche(id_table: int, nom=None, mdp=None):
    table = None
    for tab in tables:
        if tab.id == id_table:
            table = tab
    if nom is not None:
        compte = adminService().trouver_par_nom(nom)
        if not compte:
            raise HTTPException(status_code=404, detail="Compte non trouvé")
        if not compte.mdp == mdp:
            raise HTTPException(status_code=401, detail="Mot de passe erroné")
        if table is not None:
            manche = table.manche
            rev_riv = [manche.riviere[i] for i in range(5) if manche.revele[i]]
            for j in table.manche.liste_joueurs:
                if j.nom == nom:
                    return [
                f"Joueurs : {[j.nom for j in manche.liste_joueurs]}",
                f"Mise : {manche.mise}",
                f"Pot : {manche.pot}",
                f"Tour : {manche.tour}",
                f"Rivière : {rev_riv}",
                j
                ]
            raise HTTPException(status_code=404, detail="Joueur pas dans la manche")
    if table is not None:
        manche = table.manche
        rev_riv = [manche.riviere[i] for i in range(5) if manche.revele[i]]
        return [
            f"Joueurs : {[j.nom for j in manche.liste_joueurs]}",
            f"Mise : {manche.mise}",
            f"Pot : {manche.pot}",
            f"Tour : {manche.tour}",
            f"Rivière : {rev_riv}"
            ]
    else:
        raise HTTPException(status_code=404, detail="Table non trouvée")

@app.put("/manche/{table_id}", tags=["Manche"])
def jouer_manche(nom, mdp, choix: str, id_table: int, nb_jetons: int=0):
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
        if table.manche.win != "":
            return table.manche.win
        if table.manche.liste_joueurs[table.manche.tour%table.manche.n].nom == nom:
            joueur = table.manche.liste_joueurs[table.manche.tour%table.manche.n]
            if choix == "Suivre":
                joueur.suivre(table.manche)
            elif choix == "Se coucher":
                joueur.couche(table.manche)
            elif choix == "Relancer":
                joueur.relancer(nb_jetons, table.manche)
            else:
                raise HTTPException(status_code=404, detail="choix doit être 'Suivre', 'Se coucher' ou 'Relancer'")
        else:
            raise HTTPException(status_code=405, detail="Pas à ton tour")
        if table.manche.win != "":
            return table.manche.win
    else:
        raise HTTPException(status_code=404, detail="Table non trouvée")



# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876)

    logging.info("Arret du Webservice")
