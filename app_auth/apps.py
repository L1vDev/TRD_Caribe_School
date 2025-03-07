from django.apps import AppConfig


class AppAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_auth'
    verbose_name = "Usuarios"

    def ready(self):
        try:
            import app_auth.signals
        except Exception as e:
            print(e)
