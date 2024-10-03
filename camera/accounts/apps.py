from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'camera.accounts'

    def ready(self):
        from . import signals
