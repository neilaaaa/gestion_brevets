from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from apps.notifications.models import Notifications
from .models import Brevet, DemandeBrevet, Deposant, Inventeur
from apps.users.models import Utilisateur
from .serializers import (
    BrevetSerializer,
    DemandeBrevetSerializer,
    DeposantSerializer,
    InventeurSerializer,
)

User = get_user_model()

def notifier_groupe(groupe_name, message):
    """Envoie une notification à tous les users d'un groupe donné."""
    users = User.objects.filter(groups__name=groupe_name)
    for u in users:
        Notifications.objects.create(id=u, message=message)

def has_group(user, name):
    return user.groups.filter(name__iexact=name).exists()


class DemandeBrevetViewSet(viewsets.ModelViewSet):
    queryset = DemandeBrevet.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DemandeBrevetSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return DemandeBrevet.objects.all()

        if has_group(user, "responsable"):
            return DemandeBrevet.objects.all()

        if has_group(user, "directeur"):
            return DemandeBrevet.objects.all()

        return DemandeBrevet.objects.filter(id=user)

    def perform_create(self, serializer):
      statut = 'valider' if self.request.user.groups.filter(name="responsable").exists() else 'non_valider'
      demande = serializer.save(id=self.request.user, statut=statut)

      Notifications.objects.create(
       id = self.request.user,
       message=f"Votre demande '{demande.titre_dem}' a été créée avec succès."
    )
    
      notifier_groupe(
            "responsable",
            f"Nouvelle demande soumise : '{demande.titre}' par {self.request.user.username}."
        ) 
      
      if demande.id_brevet:
            Notifications.objects.create(
                id=demande.id_brevet.id,
                message=f"Un brevet a été créé pour votre demande '{demande.id_brevet.titre}'."
            )   

    @action(detail=True, methods=['post'])
    def valider_demande(self, request, pk=None):
        if not has_group(request.user, "responsable"):
            return Response(
                {"error": "Vous n'avez pas la permission de valider une demande."},
                status=status.HTTP_403_FORBIDDEN
            )

        demande = self.get_object()
        demande.statut = "valider"
        demande.save()

        Notifications.objects.create(
            id=demande.id,
            message=f"Votre demande '{demande.titre}' a ete validee."
        )

        return Response({"message": "Demande validee avec succes."})

    @action(detail=True, methods=['post'])
    def refuser_demande(self, request, pk=None):
        if not has_group(request.user, "responsable"):
            return Response(
                {"error": "Vous n'avez pas la permission de refuser une demande."},
                status=status.HTTP_403_FORBIDDEN
            )

        demande = self.get_object()
        demande.statut = "non_valider"
        demande.save()

        Notifications.objects.create(
            id=demande.id,
            message=f"Votre demande '{demande.titre}' a ete refusee."
        )

        return Response({"message": "Demande refusee avec succes."})


class DeposantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Deposant.objects.all()
    serializer_class = DeposantSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Deposant.objects.all()

        if has_group(user, "responsable"):
            return Deposant.objects.all()

        if has_group(user, "directeur"):
            return Deposant.objects.all()

        return Deposant.objects.filter(id_demande__id=user)

class InventeurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Inventeur.objects.all()
    serializer_class = InventeurSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Inventeur.objects.all()

        if has_group(user, "responsable"):
            return Inventeur.objects.all()

        if has_group(user, "directeur"):
            return Inventeur.objects.all()

        return Inventeur.objects.filter(id_demande__id=user).distinct()


class BrevetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Brevet.objects.all()
    serializer_class = BrevetSerializer


    def get_queryset(self):
     user = self.request.user
     print(f"user: {user.username}, groupes: {list(user.groups.values_list('name', flat=True))}")

     if user.is_staff or user.is_superuser:
        return Brevet.objects.all().order_by('-id_brevet')

     if user.groups.filter(name="responsable").exists():
        return Brevet.objects.all().order_by('-id_brevet')

     if user.groups.filter(name="directeur").exists():
        return Brevet.objects.all().order_by('-id_brevet')

     print("ici agent lis la ligne")
     return Brevet.objects.filter(id=user).order_by('-id_brevet')
 
    def _can_manage_brevet(self, user):
        return (
            user.is_staff
            or user.is_superuser
            or user.groups.filter(name="agent").exists()
             or user.groups.filter(name="responsable").exists()
        )

    def create(self, request, *args, **kwargs):
        if not self._can_manage_brevet(request.user):
            return Response(
                {"error": "Seul un agent peut ajouter un brevet manuellement."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not self._can_manage_brevet(request.user):
            return Response(
                {"error": "Seul un agent peut modifier un brevet."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self._can_manage_brevet(request.user):
            return Response(
                {"error": "Seul un agent peut supprimer un brevet."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)
        
    
    @action(detail=False, methods=['get'], url_path='demandes-disponibles')
    def demandes_disponibles(self, request):
        user = request.user

        if (user.is_staff or user.is_superuser or
                user.groups.filter(name="responsable").exists() or user.groups.filter(name="agent").exists()):
            demandes = DemandeBrevet.objects.filter(
               id_brevet__isnull=True,
                statut='valider'
            )
        else:
            demandes = DemandeBrevet.objects.filter(
                brevet__isnull=True,
                statut='valider',
                id=user
            )

        data = [
            {
                "id_demande": d.id_demande,
                "titre":      d.titre_dem,
                "num_depo":   d.num_depo,
                "date_depo":  d.date_depo,
            }
            for d in demandes
        ]
        return Response(data)
    
    @action(detail=True, methods=['patch'], url_path='lier-demande')
    def lier_demande(self, request, pk=None):
        if not self._can_manage_brevet(request.user):
            return Response(
                {"error": "Permission insuffisante."},
                status=status.HTTP_403_FORBIDDEN
            )

        brevet = self.get_object()
        id_demande = request.data.get('id_demande')

        if not id_demande:
            return Response(
                {"error": "id_demande est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            demande = DemandeBrevet.objects.get(id_demande=id_demande)
        except DemandeBrevet.DoesNotExist:
            return Response(
                {"error": "Demande introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifications métier
        if demande.id_brevet is not None and demande.id_brevet != brevet:
            return Response(
                {"error": "Cette demande est déjà liée à un autre brevet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if DemandeBrevet.objects.filter(id_brevet=brevet).exclude(id_demande=id_demande).exists():
            return Response(
                {"error": "Ce brevet est déjà lié à une autre demande."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Liaison : on met à jour id_brevet sur la DemandeBrevet
        demande.id_brevet = brevet
        demande.save()

        return Response(
            {
                "message": "Demande liée avec succès.",
                "id_demande": demande.id_demande,
                "titre_demande": demande.titre,
                "id_brevet": brevet.id_brevet,
            },
            status=status.HTTP_200_OK
        )
        
    @action(detail=False, methods=['get'], url_path='brevets-disponibles')
    def brevets_disponibles(self, request):
    # brevets qui n'ont pas encore de demande liée
      brevets = Brevet.objects.filter(demande__isnull=True).order_by('-id_brevet')
      data = [
        {
            "id_brevet": b.id_brevet,
            "num_brevet": b.num_brevet,
            "titre": b.titre,
        }
        for b in brevets
    ]
      return Response(data)