from django.apps import AppConfig

class VirtualClassroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'virtual_classroom'
    verbose_name = 'Virtual Classroom'

    def ready(self):
        try:
            import virtual_classroom.signals
        except ImportError:
            pass
