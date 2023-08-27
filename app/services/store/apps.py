from django.apps import AppConfig
from .mqtt import client


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services.store'

    def ready(self):
        client.loop_start()