from .models import Recours
from .serializers import RecoursSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RecoursViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Recours.objects.all()
    serializer_class = RecoursSerializer
    
    def get_queryset(self):
        # Chaque user voit seulement ses propres recours
        return Recours.objects.filter(id_user=self.request.user)
