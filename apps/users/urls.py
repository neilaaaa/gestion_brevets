from django.urls import path, include
from .views import UtilisateurViewSet, login_view, me_view, logout_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('me/', me_view, name='me'),
    path('logout/', logout_view, name='logout'),
]
