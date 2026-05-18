from rest_framework import serializers
from .models import  Document



class DocumentSerializer(serializers.ModelSerializer):
    brevet = serializers.SerializerMethodField()
    date_sortie_officielle = serializers.DateField()
    
    date_sortie_officielle = serializers.DateField(
    required=False,
    allow_null=True
)
    
    def get_brevet(self, obj):
        try:
            brevet = obj.id_brevet
            if not brevet:
                return None
            titre_invention = brevet.demande.titre if hasattr(brevet, 'demande') else brevet.titre
            return{
                "titre": obj.titre_invention,
                "num_brevet": obj.id_brevet.num_brevet
            }
        except:
            return None
        
    class Meta:
        model = Document
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate_fichier(self, value):
        if not value:
            raise serializers.ValidationError("Un document est obligatoire.")
        return value

    def validate(self, attrs):
        type_document = attrs.get("type_document")

        if type_document == "brevet" and not attrs.get("date_sortie_officielle"):
         raise serializers.ValidationError({
            "date_sortie_officielle": "Ce champ est obligatoire pour un brevet."
        })
        
        if type_document == "paiement" and not attrs.get("date_paiement",) :
         raise serializers.ValidationError({
            "montant_total": "Ce champ est obligatoire pour un paiement."
        })
         
        if type_document == "paiement" and not attrs.get("montant_total",) :
         raise serializers.ValidationError({
            "date_paiement": "Ce champ est obligatoire pour un paiement."
        })
          
        id_demande = attrs.get("id_demande")
        id_brevet = attrs.get("id_brevet")

        if not id_demande and not id_brevet:
            raise serializers.ValidationError(
                "Le document doit etre lie a une DemandeBrevet ou a un Brevet."
            )

        return attrs