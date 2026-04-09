from apps import users
from .models import Utilisateur, Role
from .serializers import RoleSerializer, UtilisateurSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count

class UtilisateurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser] # Seul l'admin peut voir tous les utilisateurs et en créer de nouveaux
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def get_queryset(self):
        # Chaque user voit seulement ses propres documents
        return Utilisateur.objects.filter(id =self.request.user.id)
    
    def get_object(self):
        # Un user peut seulement voir/modifier son propre profil
        # sauf si c'est un admin
     if self.request.user.is_staff:
        return super().get_object()
     return self.request.user

class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser] # Seul l'admin gère les rôles
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
      
     

