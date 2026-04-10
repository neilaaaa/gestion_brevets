from .models import Utilisateur
from .serializers import UtilisateurSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser


class UtilisateurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
