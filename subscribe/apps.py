from django.apps import AppConfig

class SubscribeConfig(AppConfig):
    name = 'subscribe'

    def ready(self):
        import subscribe.signals
