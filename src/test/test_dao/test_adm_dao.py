import unittest
import os
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from dao.admin_dao import adminDao
from business_object.admin import Admin
from business_object.compte import Compte


class TestAdminDaoWithRealDB(unittest.TestCase):
    """Tests du DAO admin avec une base de données de test """
    
    @classmethod
    def setUpClass(cls):
        """Préparation de la base de données de test"""
        
        dotenv.load_dotenv()
        
        # idée : Utiliser directement a bdd existante avec un schema de test
        
        cls.test_schema = "test_projet"
        
        
        cls.test_conn = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DATABASE"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            cursor_factory=RealDictCursor
        )
        cls.test_conn.autocommit = True
        
        
        with cls.test_conn.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA IF EXISTS {cls.test_schema} CASCADE;")
            cursor.execute(f"CREATE SCHEMA {cls.test_schema};")
            cursor.execute(f"SET search_path TO {cls.test_schema};")
            
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compte (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) UNIQUE NOT NULL,
                    mdp VARCHAR(255),
                    nb_jetons INTEGER DEFAULT 100,
                    nb_victoires INTEGER DEFAULT 0,
                    nb_parties INTEGER DEFAULT 0
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS adm (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) UNIQUE NOT NULL,
                    mdp VARCHAR(255) NOT NULL
                );
            """)
    
    def setUp(self):
        """Préparation avant chaque test"""
        
        with self.test_conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {self.test_schema};")
            
            
            cursor.execute("DELETE FROM compte;")
            cursor.execute("DELETE FROM adm;")
            cursor.execute("ALTER SEQUENCE compte_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE adm_id_seq RESTART WITH 1;")
            
            
            cursor.execute("""
                INSERT INTO compte (nom, mdp, nb_jetons, nb_victoires, nb_parties)
                VALUES 
                    ('joueur1', 'pass123', 100, 5, 10),
                    ('joueur2', 'pass456', 200, 3, 8);
            """)
            
            cursor.execute("""
                INSERT INTO adm (nom, mdp)
                VALUES ('admin1', 'adminpass');
            """)
        
        
        os.environ["POSTGRES_SCHEMA"] = self.test_schema
        
        
        from dao.db_connection import DBConnection
        if hasattr(DBConnection, '_instances'):
            DBConnection._instances.clear()
        
        self.dao = adminDao()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        
        os.environ["POSTGRES_SCHEMA"] = "projet"
        
        
        from dao.db_connection import DBConnection
        if hasattr(DBConnection, '_instances'):
            DBConnection._instances.clear()
    
    def test_trouver_par_nom_existant(self):
        """Test de recherche d'un compte existant"""
        compte = self.dao.trouver_par_nom("joueur1")
        
        self.assertIsNotNone(compte)
        self.assertEqual(compte.nom, "joueur1")
        self.assertEqual(compte.nb_jetons, 100)
        self.assertEqual(compte.nb_victoires, 5)
        self.assertEqual(compte.nb_parties, 10)
    
    def test_trouver_par_nom_inexistant(self):
        """Test de recherche d'un compte inexistant"""
        compte = self.dao.trouver_par_nom("inexistant")
        self.assertIsNone(compte)
    
    def test_lister_tous(self):
        """Test de listage de tous les comptes"""
        comptes = self.dao.lister_tous()
        
        self.assertEqual(len(comptes), 2)
        noms = [c.nom for c in comptes]
        self.assertIn("joueur1", noms)
        self.assertIn("joueur2", noms)
    
    def test_crediter(self):
        """Test de crédit de jetons"""
        resultat = self.dao.crediter("joueur1", 50)
        self.assertTrue(resultat)
        
        
        compte = self.dao.trouver_par_nom("joueur1")
        self.assertEqual(compte.nb_jetons, 150)
    
    def test_crediter_compte_inexistant(self):
        """Test de crédit sur un compte inexistant"""
        resultat = self.dao.crediter("inexistant", 50)
        self.assertFalse(resultat)
    
    def test_modifier_jetons(self):
        """Test de modification du nombre de jetons"""
        resultat = self.dao.modifier_jetons("joueur1", 500)
        self.assertTrue(resultat)
        
        compte = self.dao.trouver_par_nom("joueur1")
        self.assertEqual(compte.nb_jetons, 500)
    
    def test_modifier_victoires(self):
        """Test d'incrémentation des victoires et parties"""
        resultat = self.dao.modifier_victoires("joueur1")
        self.assertTrue(resultat)
        
        compte = self.dao.trouver_par_nom("joueur1")
        self.assertEqual(compte.nb_victoires, 6)
        self.assertEqual(compte.nb_parties, 11)
    
    def test_modifier_parties(self):
        """Test d'incrémentation des parties"""
        resultat = self.dao.modifier_parties("joueur2")
        self.assertTrue(resultat)
        
        compte = self.dao.trouver_par_nom("joueur2")
        self.assertEqual(compte.nb_parties, 9)
    
    def test_supprimer_existant(self):
        """Test de suppression d'un compte existant"""
        resultat = self.dao.supprimer("joueur1")
        self.assertTrue(resultat)
        
        compte = self.dao.trouver_par_nom("joueur1")
        self.assertIsNone(compte)
    
    def test_supprimer_inexistant(self):
        """Test de suppression d'un compte inexistant"""
        resultat = self.dao.supprimer("inexistant")
        self.assertFalse(resultat)
    
    def test_se_connecter_succes(self):
        """Test de connexion admin réussie"""
        admin = self.dao.se_connecter("admin1", "adminpass")
        
        self.assertIsNotNone(admin)
        self.assertEqual(admin.nom, "admin1")
        self.assertIsInstance(admin, Admin)
    
    def test_se_connecter_mauvais_mdp(self):
        """Test de connexion admin avec mauvais mot de passe"""
        admin = self.dao.se_connecter("admin1", "mauvais_mdp")
        self.assertIsNone(admin)
    
    def test_se_connecter_utilisateur_inexistant(self):
        """Test de connexion avec un utilisateur inexistant"""
        admin = self.dao.se_connecter("inexistant", "password")
        self.assertIsNone(admin)
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        
        with cls.test_conn.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA IF EXISTS {cls.test_schema} CASCADE;")
        
        cls.test_conn.close()
        
        
        os.environ["POSTGRES_SCHEMA"] = "projet"


if __name__ == '__main__':
    unittest.main()