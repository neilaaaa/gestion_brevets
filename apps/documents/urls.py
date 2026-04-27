from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet)

urlpatterns = [
  path('', include(router.urls)),
]