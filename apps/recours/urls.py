from django.urls import path, include
from . views import RecoursViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'recours', RecoursViewSet)

urlpatterns = [
    path('', include(router.urls)),
]