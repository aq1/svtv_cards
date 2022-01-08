from django.urls import (
    path,
)

from django.views.generic.base import TemplateView

from .views.upload_file import upload_file

urlpatterns = [
    path('', TemplateView.as_view(template_name='test_constructor/index.html'), name='test_constructor'),
    path('upload-file/', upload_file, name='upload_file'),
]
