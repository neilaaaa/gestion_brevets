from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.brevets.models import DemandeBrevet, Brevet
from apps.notifications.models import Notifications


class DashboardCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_model = get_user_model()

        def has_group(group_name):
            return user.groups.filter(name=group_name).exists()

        if has_group("Agent"):
            data = {
                "my_demandes": DemandeBrevet.objects.filter(id=user).count(),
                "my_brevets": Brevet.objects.filter(id=user).count(),
                "my_demandes_validees": DemandeBrevet.objects.filter(
                    id=user,
                    statut="valider"
                ).count(),
            }

        elif has_group("Responsable"):
            data = {
                "total_demandes": DemandeBrevet.objects.count(),
                "total_brevets": Brevet.objects.count(),
                "total_demandes_validees": DemandeBrevet.objects.filter(
                    statut="valider"
                ).count(),
            }

        elif has_group("Directeur"):
            data = {
                "total_demandes": DemandeBrevet.objects.count(),
                "total_brevets": Brevet.objects.count(),
                "total_demandes_validees": DemandeBrevet.objects.filter(
                    statut="valider"
                ).count(),
            }

        elif user.is_staff or user.is_superuser:
            data = {
                "total_users": user_model.objects.count(),
                "total_demandes": DemandeBrevet.objects.count(),
                "total_brevets": Brevet.objects.count(),
                "total_notifications": Notifications.objects.count(),
            }

        else:
            data = {
                "message": "Aucune statistique disponible pour ce rôle."
            }

        return Response(data)
