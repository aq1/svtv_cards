from django.contrib import admin
from django.forms import ModelForm
from django_json_widget.widgets import JSONEditorWidget
from simple_history.admin import SimpleHistoryAdmin

from ..models import PostBackup


class PostBackupForm(ModelForm):
    class Meta:
        model = PostBackup
        fields = '__all__'
        widgets = {
            'post': JSONEditorWidget(mode='tree')
        }


@admin.register(PostBackup)
class PostBackupAdmin(SimpleHistoryAdmin):
    list_display = ['ghost_id', 'updated_at', 'title']
    ordering = ['-updated_at']
    form = PostBackupForm
