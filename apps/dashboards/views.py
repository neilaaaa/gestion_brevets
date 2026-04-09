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
        role = getattr(getattr(user, "role", None), "nom_role", "")
        role = role.strip().lower()
        user_model = get_user_model()

        if role == "agent":
            data = {
                "my_demandes": DemandeBrevet.objects.filter(user=user).count(),
                "my_brevets": Brevet.objects.filter(demande__user=user).count(),
                "my_demandes_validees": DemandeBrevet.objects.filter(
                    user=user,
                    statut="valider"
                ).count(),
            }

        elif role == "responsable":
            data = {
                "total_demandes": DemandeBrevet.objects.count(),
                "total_brevets": Brevet.objects.count(),
                "total_demandes_validees": DemandeBrevet.objects.filter(
                    statut="valider"
                ).count(),
            }

        elif role == "directeur":
            data = {
                "total_demandes": DemandeBrevet.objects.count(),
                "total_brevets": Brevet.objects.count(),
                "total_demandes_validees": DemandeBrevet.objects.filter(
                    statut="valider"
                ).count(),
            }

        elif role == "admin":
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
