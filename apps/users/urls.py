from django.urls import path, include
from .views import UtilisateurViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
