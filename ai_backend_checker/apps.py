from django.apps import AppConfig

class AiBackendCheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_backend_checker'

    def ready(self):
        import ai_backend_checker.signals