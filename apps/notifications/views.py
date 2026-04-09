from .models import Notifications
from .serializers import NotificationsSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class NotificationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        return Notifications.objects.filter(id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)
