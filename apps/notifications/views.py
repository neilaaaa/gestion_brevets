from .models import Notifications
from .serializers import NotificationsSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class NotificationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        return Notifications.objects.filter(id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(id=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.etat = True
        notification.save()
        return Response({'message': 'Notification marquee comme lue avec succes.'})
