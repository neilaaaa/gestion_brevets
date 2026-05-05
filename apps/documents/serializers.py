from rest_framework import serializers
from .models import  Document



class DocumentSerializer(serializers.ModelSerializer):
    brevet = serializers.SerializerMethodField()
    
    def get_brevet(self, obj):
        try:
            return{
                "titre": obj.id_brevet.titre,
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
        id_demande = attrs.get("id_demande")
        id_brevet = attrs.get("id_brevet")

        if not id_demande and not id_brevet:
            raise serializers.ValidationError(
                "Le document doit etre lie a une DemandeBrevet ou a un Brevet."
            )

        return attrs