from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('login.urls')),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
