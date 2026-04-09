from .models import Notifications
from .serializers import NotificationsSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class NotificationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer