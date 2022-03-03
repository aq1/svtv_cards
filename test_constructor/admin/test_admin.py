from django.contrib import admin
from django.forms import fields
from django_json_widget.widgets import JSONEditorWidget

from ..models import Test


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
