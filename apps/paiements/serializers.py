from rest_framework import serializers
from .models import Paiement

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate_montant_total(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le montant total doit être strictement positif."
            )
        return value
