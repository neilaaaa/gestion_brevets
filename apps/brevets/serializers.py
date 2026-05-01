from rest_framework import serializers
from .models import DemandeBrevet, Deposant, Inventeur, Brevet
from apps.documents.serializers import DocumentSerializer

class DeposantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposant
        fields = '__all__'


class InventeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventeur
        fields = '__all__'

class BrevetSerializer(serializers.ModelSerializer):
    titre_demande_liee = serializers.SerializerMethodField() #pour afficher le num_brevet du brevet associé à la demande c'est specifique donc on utilise SerializerMethodField
    inventeur= serializers.SerializerMethodField()
    deposant =serializers.SerializerMethodField()
    
    def get_titre_demande_liee(self, obj):
        try:
            return obj.demande.titre
        except Exception as e:
            print("ERREUR get_titre_demande_liee:", e)
            return None
    
    def get_inventeur(self, obj):
        try:
            inventeurs = obj.demande.inventeurs.all()  # ← related_name="inventeurs"
            return InventeurSerializer(inventeurs, many=True).data
        except:
            return []

    def get_deposant(self, obj):
        try:
            deposants = obj.demande.deposant_set.all()  # ← pas de related_name donc deposant_set
            return DeposantSerializer(deposants, many=True).data
        except: return[]
        
    documents = DocumentSerializer(source="document_set", many=True, read_only = True)
    
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
    
class DemandeBrevetSerializer(serializers.ModelSerializer):
    num_brevet = serializers.SerializerMethodField()
    
    def get_num_brevet(self, obj):
        try:
            return obj.id_brevet.num_brevet
        except:
            return None 
    deposant = DeposantSerializer(source="deposant_set", read_only=True, many=True)
    inventeur = InventeurSerializer(source="inventeurs", read_only=True, many=True)
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

