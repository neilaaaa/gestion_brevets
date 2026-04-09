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
    
    def validate_fichier(self, value):
        # 1. Fichier obligatoire
        if not value:
            raise serializers.ValidationError("Un document est obligatoire.")