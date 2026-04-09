from .models import Paiement
from .serializers import PaiementSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class PaiementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer

    def get_queryset(self):
        return Paiement.objects.filter(id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)