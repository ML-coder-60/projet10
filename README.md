[![forthebadge](https://forthebadge.com/images/badges/cc-0.svg)](https://forthebadge.com) 

[![forthebadge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io) 
[![forthebadge](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://img.shields.io)
[![forthebadge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://img.shields.io)

# Créez une API sécurisée RESTful en utilisant Django REST

## Les fonctionalités attendues de API:

Une application de suivi des problèmes pour les trois plateformes 
(site web, applications Android et iOS).

L'application permettra essentiellement aux utilisateurs de créer divers projets, 
d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et 
d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.

Les trois applications exploiteront les points de terminaison d'API qui serviront les données.

Seuls les utilisateurs authentifiés doivent être en mesure d'accéder à quoi que ce soit dans l'application.

## Technologies

- Python 3
- Django REST Framework 
- JSON Web Token
- SQlite

## Installation de l'application

### Récupérer les sources du projet 
Tapez les commandes suivantes : 

`$ git clone https://github.com/ML-coder-60/projet10.git`

`$ cd  projet10`

### Installation/initialisation de l'environnement virtuel
 
Lancez les commandes suivantes :  

`$ virtualenv venv -p python3`

`$ source venv/bin/activate`

### Installation des composants

Tapez les commandes suivantes :

`(venv) $ pip install --upgrade pip`

`(venv) $ pip install -r requirements.txt`

## Executer L'API

Lancez la commande suivante : 

`(venv)  python softdesk/manage.py runserver`

L'application est accessible depuis url http://127.0.0.1:8000/projects/.


## Documentation 

Une documentation des points de terminaison de L'API et des exemples d'utilisation 
 sont disponibles sur cette URL https://documenter.getpostman.com/view/19223491/UVeAv9H2

## Rapport Flake8 du projet au format Html 

Un rapport de conformité est disponible dans le répertoire "flake8_report".
Pour visualiser le rapport ouvrir le fichier index.html situé dans ce répertoire
