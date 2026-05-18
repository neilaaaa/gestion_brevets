from rest_framework import serializers
from .models import DemandeBrevet, Deposant, Inventeur, Brevet
from apps.documents.serializers import DocumentSerializer
from apps.documents.models import Document
import datetime

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
    titre =serializers.SerializerMethodField()
    num_depo =serializers.SerializerMethodField()
    date_depo =serializers.SerializerMethodField()
    
    def get_num_depo(self, obj):
        try:
            return obj.demande.num_depo
        except Exception as e:
            print("ERREUR numero de depot:", e)
            return None
    
    def get_date_depo(self, obj):
        try:
            return obj.demande.date_depo
        except Exception as e:
            print("ERREUR date de depot:", e)
            return None
    
    def get_titre_demande_liee(self, obj):
        try:
            return obj.demande.titre_dem
        except Exception as e:
            print("ERREUR get_titre_demande_liee:", e)
            return None
    
    def get_titre(self, obj):
        try:
            return obj.demande.titre
        except Exception as e:
            print("ERREUR get_titre_demande_liee:", e)
            return None
    
    def get_inventeur(self, obj):
        try:
            inventeurs = obj.demande.inventeurs.all()  # related_name="inventeurs"
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
    createur_username = serializers.SerializerMethodField(read_only=True)
    createur_id       = serializers.SerializerMethodField(read_only=True)
    createur_groupe   = serializers.SerializerMethodField(read_only=True)
    documents         = serializers.SerializerMethodField(read_only=True)
    deposant          = serializers.SerializerMethodField(read_only=True)
    inventeur         = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model  = DemandeBrevet
        fields = [
            'id_demande', 'titre', 'nature', 'num_depo', 'date_depo',
            'pays_origine', 'numdemande_CA', 'date_CA', 'mandataire',
            'date_pouvoir', 'prepose_reception', 'lieu_reception',
            'date_reception', 'autre_info', 'statut', 'id',
            'piece_copie_int', 'piece_memoire_nat', 'piece_memoire_fr',
            'piece_memoire_fr_dup', 'piece_dessins_orig', 'piece_dessins_dup',
            'piece_abrege', 'piece_pouvoir', 'piece_priorite',
            'piece_cession', 'piece_titre',
            'createur_username', 'createur_id', 'createur_groupe',
            'documents', 'deposant', 'inventeur', 'id_brevet', 'titre_dem'
        ]
        extra_kwargs = {
            'id':            {'read_only': True},
            'pays_origine':  {'required': False, 'default': ''},
            'numdemande_CA': {'required': False, 'default': 0},
            'date_CA':       {'required': False},
            'date_pouvoir':  {'required': False},
            'mandataire':    {'required': False, 'default': ''},
            'num_depo':      {'required': False, 'default': 0},
            'date_depo':     {'required': False},
        }

    def get_createur_username(self, obj):
        return obj.id.username if obj.id else "—"

    def get_createur_id(self, obj):
        return obj.id.id if obj.id else None

    def get_createur_groupe(self, obj):
        if obj.id:
            groups = list(obj.id.groups.values_list('name', flat=True))
            if 'responsable' in groups:
                return 'responsable'
            if 'agent' in groups:
                return 'agent'
        return 'inconnu'

    def get_deposant(self, obj):
        deps = Deposant.objects.filter(id_demande=obj)
        return DeposantSerializer(deps, many=True).data

    def get_inventeur(self, obj):
        invs = obj.inventeurs.all()
        print(f"demande {obj.id_demande} - inventeurs: {invs}")  
        return InventeurSerializer(invs, many=True).data

    def get_documents(self, obj):
        docs    = Document.objects.filter(id_demande=obj)
        request = self.context.get('request')
        result  = []
        for doc in docs:
            fichier_url = None
            if doc.fichier:
                fichier_url = (
                    request.build_absolute_uri(doc.fichier.url)
                    if request else doc.fichier.url
                )
            result.append({
                "id_document":   doc.id_document,
                "nom_document":  doc.nom_document,
                "type_document": doc.type_document,
                "date_ajout":    str(doc.date_ajout),
                "fichier_url":   fichier_url,
                "fichier_nom":   doc.fichier.name.split("/")[-1] if doc.fichier else None,
            })
        return result

    def validate(self, data):
        today = datetime.date.today()
        if not data.get('date_CA'):      data['date_CA']      = today
        if not data.get('date_pouvoir'): data['date_pouvoir'] = today
        if not data.get('date_depo'):    data['date_depo']    = today
        return data


