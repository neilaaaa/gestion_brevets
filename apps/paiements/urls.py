from django.urls import path, include
from . views import PaiementViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'paiements', PaiementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]