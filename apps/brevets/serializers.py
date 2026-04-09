from rest_framework import serializers
from .models import DemandeBrevet, Deposant, Inventeur, Brevet

class DemandeBrevetSerializer(serializers.ModelSerializer):
  class Meta:
     model = DemandeBrevet
     fields = '__all__'

class DeposantSerializer(serializers.ModelSerializer):
  class Meta:
     model = Deposant
     fields = '__all__'
  
class InventeurSerializer(serializers.ModelSerializer):
  class Meta:
     model = Inventeur
     fields = '__all__'
     
class BrevetSerializer(serializers.ModelSerializer):
  class Meta:
     model = Brevet
     fields = '__all__'