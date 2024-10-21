from django.apps import AppConfig


class MiappCodemcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'miapp_CODEMC'
    
    def ready(self):
        import miapp_CODEMC.signals
