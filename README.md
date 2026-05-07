# SoftDesk Support API

API RESTful de gestion de tickets de support développée avec Django REST Framework.

## Authentification

L'API utilise JWT (JSON Web Token). Pour accéder aux endpoints protégés :

1. Se connecter sur /api/users/login/ pour obtenir un token
2. Ajouter le token dans le header de chaque requête :
Authorization: Bearer <ton_token>

## Permissions

- Seuls les utilisateurs authentifiés peuvent accéder à l'API
- Seuls les contributeurs d'un projet peuvent accéder à ses ressources
- Seul l'auteur d'une ressource peut la modifier ou la supprimer

## RGPD

- Vérification de l'âge lors de l'inscription (minimum 15 ans)
- Choix de consentement (can_be_contacted, can_data_be_shared)
- Droit à l'oubli (suppression du compte)

## Technologies

- Django 6.x
- Django REST Framework
- SimpleJWT
- SQLite
- Pipenv

## Prérequis

- Python 3.x
- Pipenv

## Installation

1. Cloner le repository
git clone <url_du_repo>
cd softdesk

2. Installer les dépendances
python -m pipenv install

3. Activer l'environnement virtuel
python -m pipenv shell

4. Effectuer les migrations
python manage.py migrate

5. Lancer le serveur
python manage.py runserver