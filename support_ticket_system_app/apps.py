from django.apps import AppConfig


class SupportTicketSystemAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'support_ticket_system_app'

    def ready(self):
        from django.conf import settings
        if settings.SCHEDULER:
            import sys
            if len(sys.argv) > 0 and sys.argv[1] not in ['collectstatic', 'makemigrations', 'migrate']:
                from . import scheduler
                scheduler.start()
