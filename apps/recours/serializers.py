from rest_framework import serializers
from .models import Recours

class RecoursSerializer(serializers.ModelSerializer):
    brevet = serializers.SerializerMethodField()
    
    def get_brevet(self, obj):
        try:
            return {
                "id": obj.id_brevet.id_brevet,
                "titre": obj.id_brevet.titre,
                "num_brevet": obj.id_brevet.num_brevet
            }
        except:
            return None
        
    class Meta:
        model = Recours
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }
