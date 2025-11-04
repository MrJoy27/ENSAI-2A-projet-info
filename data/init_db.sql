-----------------------------------------------------
-- Compte
-----------------------------------------------------
DROP TABLE IF EXISTS compte CASCADE ;
CREATE TABLE compte(
    id     SERIAL PRIMARY KEY,
    nom           VARCHAR(30) UNIQUE,
    mdp           VARCHAR(256),
    nb_jetons     INTEGER,
    nb_victoires  INTEGER,
    nb_parties    INTEGER
);

DROP TABLE IF EXISTS adm CASCADE ;
CREATE TABLE adm(
    nom           VARCHAR(30),
    mdp           VARCHAR(256)
);