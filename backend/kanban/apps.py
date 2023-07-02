from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KanbanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kanban'
    verbose_name = _('Kanban доска')
