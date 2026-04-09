from django.urls import path, include
from . views import NotificationsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notifications', NotificationsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]