# CRUD Dynamique (presque)


** ⚠ Quelques trucs à savoir** :
- Il s'agit d'un code **NON** correctement refactoré.
- Le back agit comme un GraphQL qui met à disposition des API en fonction de la DB (il faut quand même set les models flask)
- Le front va chercher la structure de la DB, puis affiche un crud en fonction
- Il y a une structure particulière dans l'envoie de JSON du back, qui est utilisée en front. On ne peut pas brancher le front n'importe où.

## 🕹 Fonctionnalités
- Gestion de différents types de champs (images, vidéo, musiques, textes, chiffres, date avec picker)
- Gestion de relation 1-to-N
- Gestion de relations N-to-N (avec gestion d'une table associée à la table d'association)
- Le front est entièrement dynamique en fonction de ce qu'envoie le back


## 🚂 Prochaines étapes
- Refactor le CRUD sur le backend flask
- Refactor les tests du backend (rendre modulaire)
- Refactor le front (surtout le store Vuex, faut le rendre modulaire)
- En créer un plugin Vue.js
- Trouver un moyen de générer les modèles FLASK automatiquement



## In fine ça ressemble à ça ✨
![Capture 1](/admin/static/capture_1.png)

![Capture 2](/admin/static/capture_2.png)
**Là j'ai cliqué sur une relation 1-to-N, c'est pas un bug le truc au milieu.**
**À droite ce sont les relations N-to-N qui ouvrent une fenêtre avec des switch.**

## 💪 Pour le faire marcher
- **Variables d'environnement à set**
```
APP_DIRECTORY
DATABASE_HOST
DATABASE_NAME
FRONT_URL
API_URL
PYTHONPATH=$APP_DIRECTORY:$PYTHONPATH
PROJECT_PATH=$APP_DIRECTORY/index

DATABASE_LOGIN
DATABASE_PASSWORD
FLASK_DEBUG=true
SENDGRID_API_KEY

SECURITY_PASSWORD_SALT
SECRET_KEY
```

- **Écrire des modèles Flask dans le fichier model.py (j'ai supprimé tout sauf les user, confidentialité oblige)**
- **Lancer un serveur postgresql**
- **Run les commandes classique d'installation pip (dossier server) et npm (dossier admin)**
- **Lancer les serveurs avec `npm run dev` et `python server.py`**
- **M'appeler parce que ça marche pas ou que vous avez la flemme de faire toutes ces étapes parce que c'est pas vmt fait pour être un framework ce truc** 😉 
