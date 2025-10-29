import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.compte import Compte


class compteDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux comptes de la base de données"""

    @log
    def creer(self, compte) -> bool:
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

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO compte(nom, mdp, nb_jetons, nb_victoires, nb_parties) VALUES"
                        "(%(pseudo)s, %(mdp)s, %(nb_jetons)s, %(nb_victoires)s, %(nb_parties)s)  "
                        "  RETURNING id;                                                         ",
                        {
                            "pseudo": compte.pseudo,
                            "mdp": compte.mdp,
                            "nb_jetons": compte.nb_jetons,
                            "nb_victoires": compte.nb_victoires,
                            "nb_parties": compte.nb_parties,
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
    def trouver_par_id(self, id_compte) -> Compte:
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
                        " WHERE id_compte = %(id_compte)s;  ",
                        {"id": id_compte},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        compte = None
        if res:
            compte = Compte(
                nom=res["nom"],
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
                    nom=res["nom"],
                    nb_victoires=res["nb_victoires"],
                    nb_parties=res["nb_parties"]
                )
                liste_comptes.append(compte)
        return liste_comptes

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
                        "   SET nom         = %(nom)s,                      "
                        "       mdp         = %(mdp)s,                      "
                        "       nb_jetons   = %(nb_jetons)s,                "
                        "       nb_victoires= %(nb_victoires)s,             "
                        "       nb_parties  = %(nb_parties)s                "
                        " WHERE id = %(id)s;                                ",
                        {
                            "nom": compte.nom,
                            "mdp": compte.mdp,
                            "nb_jetons": compte.nb_jetons,
                            "nb_victoires": compte.nb_victoires,
                            "nb_parties": compte.nb_parties,
                            "id": compte.id,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

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
                    # Supprimer le compte d'un compte
                    cursor.execute(
                        "DELETE FROM compte                  "
                        " WHERE id=%(id)s                    ",
                        {"id": compte.id},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def se_connecter(self, nom, mdp) -> compte:
        """se connecter grâce à son pseudo et son mot de passe

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
