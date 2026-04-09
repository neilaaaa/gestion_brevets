from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet)
router.register(r'type-documents', views.TypeDocumentViewSet)

urlpatterns = [
  path('', include(router.urls)),
]