import logging
from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection
from business_object.compte import Compte


class compteDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux comptes de la base de données"""

    @log
    def creer(self, nom, mdp) -> bool:
        """Creation d'un compte dans la base de données

        Parameters
        ----------
        compte : Compte

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """
        compte = Compte(nom=nom, mdp=mdp)
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO compte(nom, mdp, nb_jetons, nb_victoires, nb_parties) VALUES"
                        "(%(nom)s, %(mdp)s, %(nb_jetons)s, %(nb_victoires)s, %(nb_parties)s)  "
                        "  RETURNING id;                                                         ",
                        {
                            "nom": nom,
                            "mdp": mdp,
                            "nb_jetons": 0,
                            "nb_victoires": 0,
                            "nb_parties": 0,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            compte.id = res["id"]
            created = True

        return created

    @log
    def modifier(self, compte) -> bool:
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
                        "   SET    mdp = %(mdp)s                           "
                        " WHERE id = %(id)s;                                ",
                        {
                            "mdp": compte.mdp,
                            "id": compte.id,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def stats(self, nom):
        """obtenir les statistiques d'un joueur

        Parameters
        ----------
        nom : str
            nom du compte que l'on souhaite trouver

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
                        "SELECT nom, nb_victoires, nb_parties           "
                        "  FROM compte                                  "
                        " WHERE nom = %(nom)s                           ",
                        {"nom": nom},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        compte = None

        if res:
            compte = Compte(
                nom=res["nom"],
                nb_victoires=res["nb_victoires"],
                nb_parties=res["nb_parties"]
            )

        return compte

    @log
    def supprimer(self, compte) -> bool:
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
                    cursor.execute(
                        "DELETE FROM compte                                "
                        " WHERE mdp=%(mdp)s AND nom=%(nom)s                ",
                        {
                            "nom": compte.nom,
                            "mdp": compte.mdp
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def se_connecter(self, nom, mdp) -> Compte:
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
                        "  FROM compte                      "
                        " WHERE nom = %(nom)s         "
                        "   AND mdp = %(mdp)s;              ",
                        {"nom": nom, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        compte = None

        if res:
            compte = Compte(
                nom=res["nom"],
                mdp=res["mdp"],
                nb_jetons=res["nb_jetons"],
                nb_victoires=res["nb_victoires"],
                nb_parties=res["nb_parties"]
            )

        return compte
