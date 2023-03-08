pip install Django==3.2.13 --> installer Django
python -m django startproject --> créée un projet
python -m django --version --> voir la versioon

lancer le serveur --> python manage.py runserver
Projet  = plusieurs application : 

python manage.py startapp blog --> créer une appli dans le projet

Les filtres
Il existe des dizaines de filtres par défaut : safe, length, etc. Tous les filtres sont
répertoriés et expliqués dans la documentation officielle de Django :
https://docs.djangoproject.com/fr/3.2/ref/templates/builtins/.

python manage.py makemigrations --> permet de créer objet bdd
python manage.py migrate -> permet de migrer les changgements

python manage.py shell --> interpréteur