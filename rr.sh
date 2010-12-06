#!/bin/sh 
rm initial_data.json
python manage.py dumpdata > initial_data.json
python manage.py reset academico
python manage.py reset financiero
python manage.py loaddata initial_data.json
python manage.py runserver