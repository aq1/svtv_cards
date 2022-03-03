from django.contrib import admin
from django.forms import ModelForm
from django_json_widget.widgets import JSONEditorWidget

from ..models import Test


class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        widgets = {
            'json': JSONEditorWidget(mode='tree')
        }


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    form = TestForm
