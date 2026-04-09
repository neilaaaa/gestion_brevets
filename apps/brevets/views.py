from .models import DemandeBrevet, Deposant, Inventeur, Brevet
from .serializers import DemandeBrevetSerializer, DeposantSerializer, InventeurSerializer, BrevetSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class DemandeBrevetViewSet(viewsets.ModelViewSet):
    queryset =  DemandeBrevet.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DemandeBrevetSerializer
    
    def get_queryset(self):
      return DemandeBrevet.objects.filter(id_user=self.request.user) #Quand on fait un GET, retourne seulement les demandes de l’utilisateur connecté.

    def perform_create(self, serializer):
      serializer.save(id_user=self.request.user) #Quand on fait un GET, retourne seulement les demandes de l’utilisateur connecté.
    
class DeposantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Deposant.objects.all()
    serializer_class = DeposantSerializer
    
class InventeurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Inventeur.objects.all()
    serializer_class = InventeurSerializer
    
class BrevetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] # Seuls les utilisateurs connectés peuvent accéder à ces endpoints
    queryset = Brevet.objects.all()
    serializer_class = BrevetSerializer 
