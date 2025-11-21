import unittest
import os
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from dao.compte_dao import compteDao
from business_object.compte import Compte


class TestCompteDaoWithRealDB(unittest.TestCase):
    """Tests du DAO compte avec une vraie base de données de test"""
    
    @classmethod
    def setUpClass(cls):
        """Préparation de la base de données de test"""
        # Charger les variables d'environnement
        dotenv.load_dotenv()
        
        # Utiliser directement ta base de données existante
        # mais avec un schema de test
        cls.test_schema = "test_projet"
        
        # Connexion à la BDD
        cls.test_conn = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DATABASE"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            cursor_factory=RealDictCursor
        )
        cls.test_conn.autocommit = True
        
        # Créer le schema de test s'il n'existe pas
        with cls.test_conn.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA IF EXISTS {cls.test_schema} CASCADE;")
            cursor.execute(f"CREATE SCHEMA {cls.test_schema};")
            cursor.execute(f"SET search_path TO {cls.test_schema};")
            
            # Créer la table compte dans le schema de test
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compte (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) UNIQUE NOT NULL,
                    mdp VARCHAR(255),
                    nb_jetons INTEGER DEFAULT 0,
                    nb_victoires INTEGER DEFAULT 0,
                    nb_parties INTEGER DEFAULT 0
                );
            """)
    
    def setUp(self):
        """Préparation avant chaque test"""
        # Basculer sur le schema de test
        with self.test_conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.test_schema};")
            
            # Nettoyer la table
            cursor.execute("DELETE FROM compte;")
            cursor.execute("ALTER SEQUENCE compte_id_seq RESTART WITH 1;")
            
            # Insérer des données de test
            cursor.execute("""
                INSERT INTO compte (nom, mdp, nb_jetons, nb_victoires, nb_parties)
                VALUES 
                    ('pikachu', 'pika123', 100, 5, 10),
                    ('dracaufeu', 'draco456', 200, 8, 15);
            """)
        
        # Modifier temporairement le schema pour DBConnection
        os.environ["POSTGRES_SCHEMA"] = self.test_schema
        
        # IMPORTANT: Réinitialiser le Singleton pour qu'il prenne le nouveau schema
        from dao.db_connection import DBConnection
        if hasattr(DBConnection, '_instances'):
            DBConnection._instances.clear()
        
        self.dao = compteDao()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        # Remettre le schema original
        os.environ["POSTGRES_SCHEMA"] = "projet"
        
        # Réinitialiser le Singleton
        from dao.db_connection import DBConnection
        if hasattr(DBConnection, '_instances'):
            DBConnection._instances.clear()
    
    def test_creer_compte_succes(self):
        """Test de création d'un compte avec succès"""
        resultat = self.dao.creer("salamèche", "sala789")
        
        self.assertTrue(resultat)
        
        # Vérifier que le compte existe dans la BDD
        with self.test_conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.test_schema};")
            cursor.execute(
                "SELECT * FROM compte WHERE nom = 'salamèche';"
            )
            res = cursor.fetchone()
        
        self.assertIsNotNone(res)
        self.assertEqual(res["nom"], "salamèche")
        self.assertEqual(res["mdp"], "sala789")
        self.assertEqual(res["nb_jetons"], 0)
        self.assertEqual(res["nb_victoires"], 0)
        self.assertEqual(res["nb_parties"], 0)
    
    def test_creer_compte_doublon(self):
        """Test de création d'un compte avec un nom déjà existant"""
        resultat = self.dao.creer("pikachu", "autremdp")
        
        # Devrait échouer car "pikachu" existe déjà
        self.assertFalse(resultat)
    
    def test_modifier_compte_succes(self):
        """Test de modification d'un compte existant"""
        # Récupérer un compte existant
        with self.test_conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.test_schema};")
            cursor.execute(
                "SELECT * FROM compte WHERE nom = 'pikachu';"
            )
            res = cursor.fetchone()
        
        compte = Compte(
            id=res["id"],
            nom=res["nom"],
            mdp="nouveau_mdp",
            nb_jetons=res["nb_jetons"],
            nb_victoires=res["nb_victoires"],
            nb_parties=res["nb_parties"]
        )
        
        resultat = self.dao.modifier(compte)
        self.assertTrue(resultat)
        
        # Vérifier que le mot de passe a bien été modifié
        with self.test_conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.test_schema};")
            cursor.execute(
                "SELECT mdp FROM compte WHERE id = %(id)s;",
                {"id": res["id"]}
            )
            res_update = cursor.fetchone()
        
        self.assertEqual(res_update["mdp"], "nouveau_mdp")
    
    def test_modifier_compte_inexistant(self):
        """Test de modification d'un compte inexistant"""
        compte = Compte(
            id=99999,
            nom="inexistant",
            mdp="mdp",
            nb_jetons=0,
            nb_victoires=0,
            nb_parties=0
        )
        
        resultat = self.dao.modifier(compte)
        self.assertFalse(resultat)
    
    def test_supprimer_compte_succes(self):
        """Test de suppression d'un compte existant"""
        compte = Compte(
            nom="pikachu",
            mdp="pika123",
            nb_jetons=100,
            nb_victoires=5,
            nb_parties=10
        )
        
        resultat = self.dao.supprimer(compte)
        self.assertTrue(resultat)
        
        # Vérifier que le compte n'existe plus
        with self.test_conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.test_schema};")
            cursor.execute(
                "SELECT * FROM compte WHERE nom = 'pikachu';"
            )
            res = cursor.fetchone()
        
        self.assertIsNone(res)
    
    def test_supprimer_compte_mauvais_mdp(self):
        """Test de suppression avec un mauvais mot de passe"""
        compte = Compte(
            nom="pikachu",
            mdp="mauvais_mdp",
            nb_jetons=100,
            nb_victoires=5,
            nb_parties=10
        )
        
        resultat = self.dao.supprimer(compte)
        self.assertFalse(resultat)
        
        # Vérifier que le compte existe toujours
        with self.test_conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.test_schema};")
            cursor.execute(
                "SELECT * FROM compte WHERE nom = 'pikachu';"
            )
            res = cursor.fetchone()
        
        self.assertIsNotNone(res)
    
    def test_supprimer_compte_inexistant(self):
        """Test de suppression d'un compte inexistant"""
        compte = Compte(
            nom="inexistant",
            mdp="mdp",
            nb_jetons=0,
            nb_victoires=0,
            nb_parties=0
        )
        
        resultat = self.dao.supprimer(compte)
        self.assertFalse(resultat)
    
    def test_se_connecter_succes(self):
        """Test de connexion avec les bons identifiants"""
        compte = self.dao.se_connecter("pikachu", "pika123")
        
        self.assertIsNotNone(compte)
        self.assertEqual(compte.nom, "pikachu")
        self.assertEqual(compte.mdp, "pika123")
        self.assertEqual(compte.nb_jetons, 100)
        self.assertEqual(compte.nb_victoires, 5)
        self.assertEqual(compte.nb_parties, 10)
        self.assertIsInstance(compte, Compte)
    
    def test_se_connecter_mauvais_mdp(self):
        """Test de connexion avec un mauvais mot de passe"""
        compte = self.dao.se_connecter("pikachu", "mauvais_mdp")
        
        self.assertIsNone(compte)
    
    def test_se_connecter_utilisateur_inexistant(self):
        """Test de connexion avec un utilisateur inexistant"""
        compte = self.dao.se_connecter("inexistant", "password")
        
        self.assertIsNone(compte)
    
    def test_se_connecter_nom_vide(self):
        """Test de connexion avec un nom vide"""
        compte = self.dao.se_connecter("", "password")
        
        self.assertIsNone(compte)
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        # Supprimer le schema de test
        with cls.test_conn.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA IF EXISTS {cls.test_schema} CASCADE;")
        
        cls.test_conn.close()
        
        # Remettre le schema original
        os.environ["POSTGRES_SCHEMA"] = "projet"


if __name__ == '__main__':
    unittest.main()