from .models import Paiement
from .serializers import PaiementSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class PaiementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
