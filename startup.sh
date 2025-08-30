#!/bin/bash python manage.py migrate --noinput python manage.py createsuperuser --noinput --username cookie --email Virjunlargo6@Gmail.com --password Cookie12345 gunicorn apartment.wsgi --log-file - 
