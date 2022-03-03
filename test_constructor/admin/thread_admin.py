from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .test_admin import TestForm
from ..models import Thread


class ThreadForm(TestForm):
    class Meta(TestForm.Meta):
        model = Thread


@admin.register(Thread)
class ThreadAdmin(SimpleHistoryAdmin):
    form = ThreadForm
