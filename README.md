<h3 align="center">
    <img alt="Logo" title="#logo" width="250px" src="/assets/16007804386673_P10.png">
    <br>
</h3>


# OpenClassrooms Projet P12

- [Objectif](#obj)
- [Compétences](#competences)
- [Technologies](#techs)
- [Requirements](#reqs)
- [Architecture](#architecture)
- [Configuration locale](#localconfig)
- [Présentation](#presentation)

<a id="obj"></a>
## Objectif

Epic Events est une entreprise de conseil et de gestion dans l'événementiel qui répond aux besoins des start-up voulant organiser des « fêtes épiques ». L'objectif de ce projet est d'élaborer un système CRM sécurisé interne à l'entreprise.

<a id="competences"></a>
## Compétences acquises
- Élaborer l'architecture d'une base de données relationnelle
- Mettre en œuvre une base de données sécurisée avec Django ORM et PostgreSQL

<a id="techs"></a>
## Technologies Utilisées
- [Python3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [DjangoRestFramework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)

<a id="reqs"></a>
## Requirements
- django
- djangorestframework
- psycopg2-binary
- python-dotenv

<a id="architecture"></a>
## Architecture et répertoires
```
Project
├── epic
│   ├── api
│   ├── core : répertoire contenant les applications de notre CRM
│   │    ├── clients
│   │    ├── contracts
│   │    ├── events
│   │    ├── users
│   ├── epic : répertoire du projet django
│   │    ├── settings.py : fichier de réglages django
│   │    ├── urls.py : fichier principal des endpoints
│   │    ├── ..
│   ├── manage.py : fichier principal de gestion django
|── requirements.txt
|── documents
│   ├── db : dumps pour la configuration de la base de données
│   ├── postman_collections : collections Postman
│   ├── ERD.png : diagramme entité-relation
│   ├── ..
```

<a id="localconfig"></a>
## Configuration locale
## Installation

### 1. Récupération du projet sur votre machine locale

Clonez le repository sur votre machine.

```bash
git clone https://github.com/GDSDC/OpenclassroomsProject-P12.git
```

Accédez au répertoire cloné.
```bash
cd OpenclassroomsProject-P12
```

### 2. Création d'un environnement virtuel 
Créez l'environnement virtuel env.
```bash
python3 -m venv env
```

### 3. Activation et installation de votre environnement virtuel 

Activez votre environnement virtuel env nouvellement créé.
```bash
source env/bin/activate
```

Installez les paquets présents dans la liste requirements.txt.
```bash
pip install -r requirements.txt
```

### 4. Initialisation de la base de données

Installez PostgreSQL 14 via edb par example : https://www.enterprisedb.com/docs/postgresql_journey/02_installing/

Créez une base de donnée nommée '`epic_crm_db`'.

Connexion avec Django : Si besoin, vous pouvez modifier les identifiants de l'administrateur de la base de données ainsi que d'autres détails de connexion dans le fichier epi/settings.py (voir DATABASES).

Initialisez/Restorez la base de données à l'aide des dump.
```bash
psql -U <db_admin_name> -d epic_crm_db < documents/db/<dump.sql>
```
_<db_admin_name>_ : renseignez le nom de votre administrateur de base de données (généralement _postrgre_)

_<dump.sql>_ : vous pouvez choisir d'initialiser/restaurer la base de données à l'aide des documents/db/dumps suivantes :
* `epic_crm_db_init.sql` -> base initiale peuplée uniquement d'un superuser (email=admin@admin.com / mdp=admin).
* `epic_crm_db_example.sql` -> base peuplée de quelques données pour démonstration.

## Utilisation

### 1. Démarrage du serveur local

Accédez au dossier de travail.
```bash
cd epic
```

Démarrez le serveur local.
```bash
python manage.py runserver
```

Retrouvez des exemples de requêtes http en important sur Postman la collection documents/postman_collections/P12_epic_crm_api.postman_collection.json.

<a id="presentation"></a>
### Présentation

[<img alt="presentation" width="480px" src="/assets/presentation.png">](https://docs.google.com/presentation/d/e/2PACX-1vQdHqIKs6YUb5Qyri8rIGuURQLU5yvs9xVZcI4BmV5vMw66hsqEFeAadzbF8ocgHJvwm0VIXmoVBNI5/pub?start=false&loop=false&delayms=5000)