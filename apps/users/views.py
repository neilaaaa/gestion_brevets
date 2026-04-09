from .models import Utilisateur, Role
from .serializers import RoleSerializer, UtilisateurSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

class UtilisateurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
