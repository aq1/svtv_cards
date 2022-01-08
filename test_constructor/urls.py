from django.urls import (
    path,
)

from django.views.generic.base import TemplateView

from .views.upload_file import upload_file
from .views.save_test import save_test
from .views.get_tests import get_tests

urlpatterns = [
    path('', TemplateView.as_view(template_name='test_constructor/index.html'), name='test_constructor'),
    path('upload-file/', upload_file, name='upload_file'),
    path('save-test/', save_test, name='save_test'),
    path('tests/', get_tests, name='get_tests'),
]
