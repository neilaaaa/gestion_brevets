from .models import DemandeBrevet, Deposant, Inventeur, Brevet
from .serializers import DemandeBrevetSerializer, DeposantSerializer, InventeurSerializer, BrevetSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class DemandeBrevetViewSet(viewsets.ModelViewSet):
    queryset = DemandeBrevet.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DemandeBrevetSerializer

    def get_queryset(self):
        return DemandeBrevet.objects.filter(id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)

    @action(detail=True, methods=['post'])
    def valider_demande(self, request, pk=None):
        if not request.user.groups.filter(name="Responsable").exists():
            return Response(
                {"error": "Vous n'avez pas la permission de valider une demande."},
                status=status.HTTP_403_FORBIDDEN
            )

        demande = self.get_object()
        demande.statut = 'valider'
        demande.save()
        return Response({'message': 'Demande validée avec succès.'})

    @action(detail=True, methods=['post'])
    def refuser_demande(self, request, pk=None):
        if not request.user.groups.filter(name="Responsable").exists():
            return Response(
                {"error": "Vous n'avez pas la permission de refuser une demande."},
                status=status.HTTP_403_FORBIDDEN
            )

        demande = self.get_object()
        demande.statut = 'non_valider'
        demande.save()
        return Response({'message': 'Demande refusée avec succès.'})


class DeposantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Deposant.objects.all()
    serializer_class = DeposantSerializer


class InventeurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Inventeur.objects.all()
    serializer_class = InventeurSerializer


class BrevetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Brevet.objects.all()
    serializer_class = BrevetSerializer
