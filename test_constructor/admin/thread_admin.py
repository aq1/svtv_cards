from django.contrib import admin
from django.forms import fields
from django_json_widget.widgets import JSONEditorWidget
from simple_history.admin import SimpleHistoryAdmin

from ..models import Thread


@admin.register(Thread)
class ThreadAdmin(SimpleHistoryAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
