# minesweeper

Minesweeper game implementation as a JSON REST service.
Implemented with Django REST framework and PostgreSQL.

##Development environment
Requires Docker and Docker Composer. Scripts to create/start/stop the service are in `/scripts/`

##First Run
```
python manage.py migrate auth
python manage.py migrate
python manage.py createsuperuser
```
##Service start
```
python manage.py runserver
```
