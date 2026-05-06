from .models import Paiement
from .serializers import PaiementSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class PaiementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Paiement.objects.all().order_by('id_paiement')
    serializer_class = PaiementSerializer

    def get_queryset(self):
     user = self.request.user

     if user.is_staff or user.is_superuser:
        return Paiement.objects.all().order_by('id_paiement')

     if user.groups.filter(name="directeur").exists():
        return Paiement.objects.all().order_by('id_paiement')

     if user.groups.filter(name="responsable").exists():
        return Paiement.objects.all().order_by('id_paiement')

     return Paiement.objects.filter(id=self.request.user).order_by('id_paiement')

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)