from django.http import FileResponse, Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Document
from apps.paiements.models import  Paiement
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        user = self.request.user
        brevet_id = self.request.query_params.get('brevet')
        
        if brevet_id:
            return Document.objects.filter(id_brevet=brevet_id)

        if user.is_staff or user.is_superuser:
            return Document.objects.all()

        if user.groups.filter(name="responsable").exists():
            return Document.objects.all()

        if user.groups.filter(name="directeur").exists():
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
        document = serializer.save(id=self.request.user)
        print("DATA reçue:", self.request.data)
        
        if document.type_document == "brevet" and document.id_brevet:
            document.id_brevet.statut = "ACCEPTER"
            if document. date_sortie_officielle: 
             document.id_brevet.date_sortie = document. date_sortie_officielle
            document.id_brevet.save()
            
        if document.type_document == "paiement":
         paiement_existant = Paiement.objects.filter(id_brevet=document.id_brevet).first()
         if paiement_existant:
            paiement_existant.date_paiement = document.date_paiement
            paiement_existant.montant_total = document.montant_total
            paiement_existant.statut = "payé"
            paiement_existant.save()
            document.id_paiement = paiement_existant
         else:
            paiement = Paiement.objects.create(
                id_brevet=document.id_brevet,
                date_paiement=document.date_paiement,
                montant_total=document.montant_total,
                statut="payé",
                id=self.request.user
            )
            document.id_paiement = paiement
        
         document.save()
            
    def perform_update(self, serializer):
        document = serializer.save()
        
        if document.type_document == "brevet" and document.id_brevet:
            document.id_brevet.statut = "ACCEPTER"
            if document. date_sortie_officielle: 
             document.id_brevet.date_sortie = document. date_sortie_officielle
            document.id_brevet.save()
            
        if document.type_document == "paiement" and document.id_paiement:
         paiement = document.id_paiement
         paiement.date_paiement = document.date_paiement
         paiement.montant_total = document.montant_total
         if document.id_brevet:
            paiement.id_brevet = document.id_brevet
         paiement.save()
             
             
    def perform_destroy(self, instance):
        brevet    = instance.id_brevet
        paiement  = instance.id_paiement
        type_doc  = instance.type_document

        instance.delete()

        if type_doc == "brevet" and brevet:
            reste = Document.objects.filter(
                id_brevet=brevet,
                type_document="brevet"
            ).exists()
            if not reste:
                brevet.statut = "REFUSER"
                brevet.save()

        # Type "paiement" supprimé → si plus aucun doc paiement sur ce brevet → "non_paye"
        if type_doc == "paiement" and brevet:
            reste = Document.objects.filter(
                id_brevet=brevet,
                type_document="paiement"
            ).exists()
            if not reste and paiement:
                paiement.statut = "non_paye"
                paiement.save()
                
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

