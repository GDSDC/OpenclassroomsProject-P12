# OpenclassroomsProject-P12
OpenClassRooms Project-P12 est un projet Python ayant un but d'apprentissage dans le cadre de la formation OpenClassRooms Développeur d'Application Python.  
Thème du projet : Développez une architecture back-end sécurisée en utilisant Django ORM


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

Créez une base de donnée nommée 'epic_crm_name'.

Connexion avec Django : Si besoin, vous pouvez modifier les identifiants de l'administrateur de la base de données ainsi que d'autres détails de connexion dans le fichier epi/settings.py (voir DATABASES).

Initialisez/Restorez la base de données à l'aide des dump.
```bash
psql -U <db_admin_name> -d epic_crm_db < documents/db/<dump.sql>
```
_<db_admin_name>_ : renseignez le nom de votre administrateur de base de données (généralement _postrgre_)

_<dump.sql>_ : vous pouvez choisir d'initialiser/restaurer la base de données à l'aide des documents/db/dumps suivantes :
* epic_crm_db_init.sql -> base initiale peuplée uniquement d'un superuser (email=admin@admin.com / mdp=admin).
* epic_crm_db_example.sql -> base peuplée de quelques données pour démonstration.

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
