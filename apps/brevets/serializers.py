from rest_framework import serializers
from .models import DemandeBrevet, Deposant, Inventeur, Brevet
from apps.documents.serializers import DocumentSerializer

class DemandeBrevetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeBrevet
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'statut': {'read_only': True},
        }

    def validate(self, attrs):
        date_depo = attrs.get("date_depo")
        date_reception = attrs.get("date_reception")

        if date_depo and date_reception and date_reception < date_depo:
            raise serializers.ValidationError(
                "La date de reception ne peut pas etre anterieure a la date de depot."
            )

        return attrs


class DeposantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposant
        fields = '__all__'


class InventeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventeur
        fields = '__all__'


class BrevetSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(source="document_set", many=True, read_only = True)
    id_inv= InventeurSerializer(many=True, read_only=True)
    id_dep = DeposantSerializer(read_only=True)
    
    class Meta:
        model = Brevet
        fields = '__all__'
        extra_kwargs = {
            'id_brevet': {'read_only': True},
            'id': {'read_only': True},
            'user':{'read_only': True},
        }

    def validate(self, attrs):
        date_depo = attrs.get("date_depo")
        date_sortie = attrs.get("date_sortie")

        if date_depo and date_sortie and date_sortie < date_depo:
            raise serializers.ValidationError(
                "La date de sortie ne peut pas etre anterieure a la date de depot."
            )

        return attrs
