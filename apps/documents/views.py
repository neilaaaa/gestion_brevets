from django.http import FileResponse, Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Document.objects.all()

        if user.groups.filter(name="Responsable").exists():
            return Document.objects.all()

        if user.groups.filter(name="Directeur").exists():
            return Document.objects.all()

        return Document.objects.filter(id=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        id_demande = request.data.get("demande")
        id_brevet = request.data.get("id_brevet")

        if not (
            user.is_staff
            or user.is_superuser
            or user.groups.filter(name="responsable").exists()
            or user.groups.filter(name="directeur").exists()
        ):
            if id_demande:
                from apps.brevets.models import DemandeBrevet
                allowed_demande = DemandeBrevet.objects.filter(
                    id_demande=id_demande,
                    id=user
                ).exists()

                if not allowed_demande:
                    return Response(
                        {"error": "Vous ne pouvez pas lier ce document a une demande qui ne vous appartient pas."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            if id_brevet:
                from apps.brevets.models import Brevet
                allowed_brevet = Brevet.objects.filter(
                    id_brevet=id_brevet,
                    id_id=user
                ).exists()

                if not allowed_brevet:
                    return Response(
                        {"error": "Vous ne pouvez pas lier ce document a un brevet hors de votre perimetre."},
                        status=status.HTTP_403_FORBIDDEN
                    )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)
        print("DATA reçue:", self.request.data)
        document = serializer.save()
        
        if document.type_document == "brevet" and document.id_brevet:
            document.id_brevet.statut = "ACCEPTER"
            if document. date_sortie_officielle: 
             document.id_brevet.date_sortie = document. date_sortie_officielle
            document.id_brevet.save()
            
        if document.type_document == "paiement" and document.id_brevet:
            try:
             paiement = document.id_brevet.paiement
             paiement.statut = "payer"
             paiement.save()
            except:
                pass
            
    def perform_update(self, serializer):
        document = serializer.save()
        if document.type_document == "brevet" and document.id_brevet:
            document.id_brevet.statut = "ACCEPTER"
            if document. date_sortie_officielle: 
             document.id_brevet.date_sortie = document. date_sortie_officielle
            document.id_brevet.save()
            
        if document.type_document == "paiement" and document.id_paiement:
             document.id_paiement.statut = "payer"
             document.id_paiement.save()

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        document = self.get_object()

        if not document.fichier:
            raise Http404("Fichier introuvable.")

        return FileResponse(
            document.fichier.open("rb"),
            as_attachment=True,
            filename=document.fichier.name.split("/")[-1]
        )

