from django.apps import AppConfig


class AppCommerceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.app_channels"

    def ready(self):
        try:
            import apps.app_channels.signals  # type: ignore # noqa: F401
        except ImportError:
            pass
