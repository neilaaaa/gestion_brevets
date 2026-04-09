from rest_framework import serializers
from .models import Notifications

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }
