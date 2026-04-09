from rest_framework import serializers
from .models import Recours

class RecoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recours
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }
