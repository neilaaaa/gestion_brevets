from rest_framework import serializers
from .models import Recours

class RecoursSerializer(serializers.ModelSerializer):
  class Meta:
    model = Recours
    fields = '__all__'