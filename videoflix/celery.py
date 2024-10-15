from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Setze das Django-Settings-Modul für Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix.settings')

app = Celery('videofix_back')

# Verwende die Einstellungen in Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tasks automatisch laden
app.autodiscover_tasks()























