from django.urls import (
    path,
)
from django.views.generic.base import TemplateView

from .views.get_tests import get_tests
from .views.get_threads import get_threads
from .views.save_test import save_test
from .views.save_thread import save_thread
from .views.upload_file import upload_file
from .views.upload_video import upload_video

urlpatterns = [
    path('tests', TemplateView.as_view(template_name='test_constructor/index.html'), name='test_constructor'),
    path('threads', TemplateView.as_view(template_name='test_constructor/index.html'), name='thread_constructor'),
    path('upload-file/', upload_file, name='upload_file'),
    path('upload-video/', upload_video, name='upload_video'),
    path('save-test/', save_test, name='save_test'),
    path('save-thread/', save_thread, name='save_thread'),
    path('tests/', get_tests, name='get_tests'),
    path('threads/', get_threads, name='get_threads'),
]
