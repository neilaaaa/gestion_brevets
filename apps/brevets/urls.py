from django.urls import path, include
from . views import DemandeBrevetViewSet, DeposantViewSet, InventeurViewSet, BrevetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'demandes', DemandeBrevetViewSet)
router.register(r'deposants', DeposantViewSet)
router.register(r'inventeurs', InventeurViewSet)
router.register(r'brevets', BrevetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]