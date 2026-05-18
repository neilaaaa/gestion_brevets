from rest_framework import serializers
from .models import Paiement


class PaiementSerializer(serializers.ModelSerializer):
    brevet = serializers.SerializerMethodField()

    def get_brevet(self, obj):
        try:
            brevet = obj.id_brevet
            demande = getattr(brevet, "demande", None)
            titre = (
                getattr(brevet, "titre", None)
                or getattr(demande, "titre", None)
                or getattr(demande, "titre_dem", None)
                or ""
            )
            return {
                "titre": titre,
                "num_brevet": brevet.num_brevet,
            }
        except:
            return None

    class Meta:
        model = Paiement
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True}
        }

    def validate_montant_total(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le montant total doit etre strictement positif."
            )
        return value