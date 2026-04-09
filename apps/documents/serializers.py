from rest_framework import serializers
from .models import TypeDocument, Document

class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDocument
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
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
                "Le document doit être lié à une DemandeBrevet ou à un Brevet."
            )

        return attrs
