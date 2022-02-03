from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path,
    include,
)

from django.conf import settings

urlpatterns = [
    path('', include('webhooks.urls')),
    path('webhook/admin/', admin.site.urls),
    path('constructors/', include('test_constructor.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

