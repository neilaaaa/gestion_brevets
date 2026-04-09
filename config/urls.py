from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('', include('apps.documents.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.brevets.urls')),
    path('', include('apps.dashboards.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Gestion des Brevets"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Bienvenue"