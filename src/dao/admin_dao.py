import logging
from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection
from business_object.compte import Compte
from business_object.admin import Admin
from typing import Optional

class adminDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux comptes de la base de données"""

    @log
    def trouver_par_nom(self, nom_compte) -> Compte:
        """trouver un compte grace à son id

        Parameters
        ----------
        id_compte : int
            numéro id du compte que l'on souhaite trouver

        Returns
        -------
        compte : Compte
            renvoie le compte que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM compte                      "
                        " WHERE nom = %(nom_compte)s;  ",
                        {"nom_compte": nom_compte},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        compte = None
        if res:
            compte = Compte(
                nom=res["nom"],
                nb_jetons=res["nb_jetons"],
                nb_victoires=res["nb_victoires"],
                nb_parties=res["nb_parties"]
            )

        return compte

    @log
    def lister_tous(self) -> list[Compte]:
        """lister tous les comptes

        Parameters
        ----------
        None

        Returns
        -------
        liste_comptes : list[Compte]
            renvoie la liste de tous les comptes dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM compte;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_comptes = []

        if res:
            for row in res:
                compte = Compte(
                    id=row["id"],
                    nom=row["nom"],
                    nb_jetons=row["nb_jetons"],
                    nb_victoires=row["nb_victoires"],
                    nb_parties=row["nb_parties"]
                )
                liste_comptes.append(compte)
        return liste_comptes

    @log
    def crediter(self, nom, nb_jetons) -> bool:
        """Modification d'un compte dans la base de données

        Parameters
        ----------
        compte : Compte

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE compte                                      "
                        "   SET nb_jetons   = nb_jetons + %(nb_jetons)s     "
                        " WHERE nom = %(nom)s;                                ",
                        {
                            "nb_jetons": nb_jetons,
                            "nom": nom,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    def modifier_victoires(self, nom):
        """Modification d'un compte dans la base de données

        Parameters
        ----------
        compte : Compte

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE compte                                      "
                        "   SET nb_victoires   = nb_victoires + 1           "
                        "       nb_parties     = nb_parties + 1             "
                        " WHERE nom = %(nom)s;                              ",
                        {
                            "nom": nom,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    def modifier_parties(self, nom):
        """Modification d'un compte dans la base de données

        Parameters
        ----------
        compte : Compte

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE compte                                      "
                        "   SET nb_parties   = nb_parties + 1               "
                        " WHERE nom = %(nom)s;                              ",
                        {
                            "nom": nom,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def supprimer(self, nom) -> bool:
        """Suppression d'un compte dans la base de données

        Parameters
        ----------
        compte : Compte
            compte à supprimer de la base de données

        Returns
        -------
            True si le compte a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer un compte
                    cursor.execute(
                        "DELETE FROM compte                    "
                        " WHERE nom=%(nom)s                    ",
                        {"nom": nom},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def se_connecter(self, nom, mdp) -> Admin:
        """se connecter grâce à son nom et son mot de passe

        Parameters
        ----------
        nom : str
            nom du compte que l'on souhaite trouver
        mdp : str
            mot de passe du compte

        Returns
        -------
        compte : compte
            renvoie le compte que l'on cherche
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM adm                         "
                        " WHERE nom = %(nom)s               "
                        "   AND mdp = %(mdp)s;              ",
                        {"nom": nom, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        admin = None

        if res:
            admin = Admin(
                nom=res["nom"],
                mdp=res["mdp"],
            )

        return admin
