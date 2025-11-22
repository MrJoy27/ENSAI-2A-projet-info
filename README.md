## Poker-Server – ENSAI 2A Project

This project implements a Texas Hold’em Poker Server capable of hosting tables, managing players, 
enforcing poker rules, and communicating with users via HTTP.


The application includes:

- Layered architecture (DAO, service, view, business_object)
- Connection to a PostgreSQL database
- Terminal user interface 
- A REST webservice for clients to interact with the poker server
- Tools for logs, database initialization, and unit tests


## :arrow_forward: Software and tools

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- A [PostgreSQL](https://www.postgresql.org/) database


## :arrow_forward: Clone the repository

STEPS : 

 Open VSCode in Onyxia (using the port 9876)
 Open a Git Bash terminal 
 Clone your repository using the command : 
git clone https://github.com/MrJoy27/ENSAI-2A-projet-info.git

THEN :

Open Folder
 Open Visual Studio Code
 File > Open Folder
 Select your project folder > ok 

 PS:
- The project folder must be the root in your Explorer redo the steps if it is not ! 

## :warning: If not, the application will not launch. Retry Open Folder.

---

## Repository Files Overview :

| Item        | Description                                                         |
| ----------- | ------------------------------------------------------------------- |
| `README.md` | Provides all information needed to install and use the Poker Server |
| `LICENSE`   | Specifies the usage rights and licensing terms for the repository   |




- Configuration files :

This repository contains several configuration files for tooling.
Normally, you will not need to modify any file except .env


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

You generally do not need to modify configuration files except for .env 


## :arrow_forward: Install required packages

 In Git Bash, run the following to install required Python packages and list them:

```bash 
pip install -r requirements.txt
pip list
```

## :arrow_forward: Environment variables

You must define environment variables describing:

- the database connection
- the host of the webservice

At the root of the project:
 Create a file named .env (don't forget the . at the beginning)

 Go to https://datalab.sspcloud.fr/ (Onyxia) and create a new service : Postgresql and copy the identifications 


  THEN : 

 Paste and complete the values below:

```bash
WEBSERVICE_HOST=your webservice url on onyxia

POSTGRES_HOST=sgbd-eleves.domensai.ecole
POSTGRES_PORT=5432
POSTGRES_DATABASE=idxxxx
POSTGRES_USER=idxxxx
POSTGRES_PASSWORD=idxxxx
POSTGRES_SCHEMA=projet
```
* Ps keep in mind : 

- Hostname : POSTGRES_HOST
- Port : POSTGRES_PORT
- Database : POSTGRES_DATABASE
- Username : POSTGRES_USER
- Password : POSTGRES_PASSWORD



This will allow the Poker Server to authenticate players, store their balances, manage tables, and run games.



## :arrow_forward: Unit tests
TESTING PHASE :

 In Git Bash, write : 

```bash
pytest -v
```


or:
```bash  ,

python -m pytest -v
```
- TU DAO :

To ensure safe and repeatable tests that do not modify production data, DAO tests load their data 
into a dedicated schema.

* The DAO test data comes from:

data/pop_db_test.sql

It is loaded into a separate schema:

test/test_dao

* Test coverage (optional):

Test coverage can be generated with Coverage:
```bash
 coverage run -m pytest
 coverage report -m
 coverage html
```

Open the file coverage_report/index.html in your browser.

## :arrow_forward: Launch the webservice

The webservice exposes a REST API allowing:

- Player account creation and authentication
- Joining tables
- Taking poker actions
- Getting current table/game state
- Admin operations



- To launch the webservice:

```bash
python src/app.py
```

To launch the app go to My Services in the Onyxia datalab and press 

*Open* > use the link (second link in the description paragraph )to connect to the 9876 
port ( !! DO NOT COPY THE PASSWORD AND CONNECT LIKE WE USUALLY DO !! )


## :arrow_forward: Launch the TUI application

The CLI allows players or admins to interact with the poker server through a text-based menu system. It has to be launched when the webservice is launched in a another terminal

.

SO: 

 In Git Bash :
```bash
python src/main.py
```

On first launch, choose Reset database:

This runs src/utils/reset_database.py

It executes all SQL initialization scripts placed in data/
Using the terminal, 

players may:

- Log in / sign in 
- Join a table
- Take actions during their turn (fold/call/raise/all-in)
- View their wallet balance
- Check the statistics (wins / games played)

Admins may:

- Credit player balances
- ban an account 



## :arrow_forward: Logs

Logs are initialized in the file:
```bash
src/utils/log_init.py
```

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

```bash
06/11/2025 13:22:16 - INFO     - --------------------------------------------------
06/11/2025 13:22:16 - INFO     - Lancement Application                           
06/11/2025 13:22:16 - INFO     - --------------------------------------------------
06/11/2025 13:22:16 - INFO     - AccueilVue
06/11/2025 13:22:24 - INFO     - ConnexionVue
06/11/2025 13:22:28 - INFO     -     compteService.se_connecter('a', '*****') - DEBUT
06/11/2025 13:22:28 - INFO     -         compteDao.se_connecter('a', '*****') - DEBUT
```
