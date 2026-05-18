from rest_framework import serializers
from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    brevet = serializers.SerializerMethodField()
    date_paiement = serializers.SerializerMethodField()
    montant_total = serializers.SerializerMethodField()



    def get_brevet(self, obj):
        try:
            return{
                "titre": obj.id_brevet.titre,
                "num_brevet": obj.id_brevet.num_brevet
            }
        except:
            return None
        
    def get_date_paiement(self, obj):
        try:
            return obj.document.date_paiement  # via OneToOne
        except:
            return None

    def get_montant_total(self, obj):
        try:
            return obj.document.montant_total
        except:
            return None
    
    
    class Meta:
        model = Paiement
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate_montant_total(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le montant total doit etre strictement positif."
            )
        return value
