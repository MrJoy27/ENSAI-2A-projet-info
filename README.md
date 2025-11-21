## Poker-Server – ENSAI 2A Project

This project implements a Texas Hold’em Poker Server capable of hosting tables, managing players, 
enforcing poker rules, and communicating with users via HTTP.


The application includes:

- Layered architecture (DAO, service, view, business_object)
- Connection to a PostgreSQL database
- Terminal interface 
- A REST webservice for clients to interact with the poker server
- Terminal-based interactive interface 
- Tools for logs, database initialization, and unit tests


## :arrow_forward: Software and tools

- Visual Studio Code
- Python 3.13
- Git
- PostgreSQL database
#### An API testing tool such as Insomnia or Postman ?


## arrow_forward: Clone the repository

STEPS : 

 Open VSCode
 Open a Git Bash terminal 
 Clone your repository using the command : 
git clone <your-repository-url>

THEN :

Open Folder
 Open Visual Studio Code
 File > Open Folder
 Select your project folder > ok 

 PS:
- The project folder must be the root in your Explorer redo the steps if it is not ! 

## :warning !! : If not, the application will not launch. Retry Open Folder.

---

## Repository Files Overview :

| Item        | Description                                                         |
| ----------- | ------------------------------------------------------------------- |
| `README.md` | Provides all information needed to install and use the Poker Server |
| `LICENSE`   | Specifies the usage rights and licensing terms for the repository   |




- Configuration files :

This repository contains several configuration files for tooling.
Normally, you will not need to modify any file except:

-  .env
-  requirements.txt


* Item	Description :

| Item                       | Description                                                    |
| -------------------------- | -------------------------------------------------------------- |
| `.github/workflows/ci.yml` | Continuous Integration pipeline (tests, linting, installation) |
| `.vscode/settings.json`    | VSCode workspace settings                                      |
| `.coveragerc`              | Coverage configuration                                         |
| `.gitignore`               | Ignored files and folders                                      |
| `logging_config.yml`       | Logging configuration                                          |
| `requirements.txt`         | Python package list                                            |




You will also need a .env file (see below).


* Folders :

| Item   | Description                                                       |
| ------ | ----------------------------------------------------------------- |
| `data` | SQL scripts for initializing poker tables, players, and test data |
| `doc`  | UML diagrams and project documentation                            |
| `logs` | Generated log files (created after first application launch)      |
| `src`  | Main application source code following a layered architecture     |


* Settings files :

(Same as above)

You generally do not need to modify configuration files except for .env and possibly 
requirements.txt (only if you don't have the versions mentioned above of python and other softwares)


## :arrow_forward: Install required packages

 In Git Bash, run the following to install required Python packages and list them:

pip install -r requirements.txt
pip list


## :arrow_forward: Environment variables

You must define environment variables describing:

- the database connection
- the host of the webservice

At the root of the project:
 Create a file named .env (don't forget the . at the beginning)

  THEN : 

 Paste and complete the values below:


WEBSERVICE_HOST=https://pokeapi.co/api/v2

POSTGRES_HOST= postgresql-563160.user-rouabenyoussef
POSTGRES_PORT= 5432
POSTGRES_DATABASE= defaultdb
POSTGRES_USER= user-rouabenyoussef
POSTGRES_PASSWORD= 4qh42r51fbhaufn4nmgr


POSTGRES_SCHEMA=projet


This will allow the Poker Server to authenticate players, store their balances, manage tables, and run games.



## :arrow_forward: Unit tests
TESTING PHASE :

 In Git Bash, write : 


pytest -v



or:


python -m pytest -v

- TU DAO :

To ensure safe and repeatable tests that do not modify production data, DAO tests load their data 
into a dedicated schema.

* The DAO test data comes from:

data/pop_db_test.sql

It is loaded into a separate schema:

test/test_dao

* Test coverage (optional):

Test coverage can be generated with Coverage:

 coverage run -m pytest
 coverage report -m
 coverage html

Open the file coverage_report/index.html in your browser.


## :arrow_forward: Launch the CLI application

The CLI allows players or admins to interact with the poker server through a text-based menu system.

SO: 

 In Git Bash :

python src/main.py


On first launch, choose Reset database:

This runs src/utils/reset_database.py

It executes all SQL initialization scripts placed in data/
Using the terminal, 

* players may:

Log in
Join a table
Take actions during their turn (fold/call/raise/all-in)
View their wallet balance

* Admins may:

Credit player balances
Manage tables
:arrow_forward: Launch the webservice
The webservice exposes a REST API allowing:
Player account creation and authentication
Joining tables
Taking poker actions
Getting current table/game state
Admin operations



- To launch the webservice:

python src/app.py

* Documentation:

/docs (Swagger UI)
/redoc (alternative documentation)

* Endpoints

Here are examples of endpoints (test them with Insomnia, Postman, or a browser):
Players
GET http://localhost:8000/joueur
GET http://localhost:8000/joueur/3


- Bash - 

POST http://localhost:8000/joueur/
JSON body :
{
  "nom": "a",
  "mdp": "a"
}

-----

PUT http://localhost:8000/joueur/3
JSON body :
{
   "pseudo": "tartiflette",
   "mdp": 1234
}


-------

DELETE http://localhost:8000/joueur/5



- Tables & Poker Gameplay :

(this project may expose routes such as:)

POST http://localhost:8000/table/1/join
POST http://localhost:8000/table/1/action
GET http://localhost:8000/table/1/state

These allow joining seats, playing turns, and querying game state.


## :arrow_forward: Logs

Logs are initialized in the file:

src/utils/log_init.py

It is executed when launching either the CLI or the webservice.

It uses logging_config.yml for configuration (log level, format, etc.).
we also have :

- A decorator in   src/utils/log_decorator.py
- automatically logs
- Function input parameters
- Return values
- Start and end timestamps
Logs are stored in the logs folder.


Example of logs: 

06/11/2025 13:22:16 - INFO     - --------------------------------------------------
06/11/2025 13:22:16 - INFO     - Lancement Application                           
06/11/2025 13:22:16 - INFO     - --------------------------------------------------
06/11/2025 13:22:16 - INFO     - AccueilVue
06/11/2025 13:22:24 - INFO     - ConnexionVue
06/11/2025 13:22:28 - INFO     -     compteService.se_connecter('a', '*****') - DEBUT
06/11/2025 13:22:28 - INFO     -         compteDao.se_connecter('a', '*****') - DEBUT



## :arrow_forward: Continuous integration (CI)

The repository includes a .github/workflows/ci.yml file.


On every GitHub push, a CI pipeline starts:

- Creates an Ubuntu environment
- Installs Python
- Installs all dependencies
- Runs unit tests (mainly service-layer tests)
- Runs pylint

If score < 7.5, the pipeline fails
You can follow CI progress on GitHub under the *Actions* tab.