from django.urls import (
    path,
)

from django.views.generic.base import TemplateView

urlpatterns = [
    path('test-constructor/', TemplateView.as_view(template_name='test_constructor/index.html'), name='test-constructor'),
]
