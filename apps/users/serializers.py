from rest_framework import serializers
from .models import Role, Utilisateur

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        
class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = 'id','date_ajout', 'id_role'
        read_only_fields = 'date_ajout', 'id_role'
        extra_kwargs = {
       'password': {'write_only': True}
        } #cache le password dans les réponses de l'API et aussi pour éviter les erreurs de validation lors de la création d'un utilisateur avec un mot de passe haché déjà existant dans la base de données.
        
    def create(self, validated_data):
        password = validated_data.pop('password', None) #récupère le mot de passe brut du validated_data et le supprime du dictionnaire pour éviter les erreurs de validation lors de la création d'un utilisateur avec un mot de passe haché déjà existant dans la base de données.
        user = super().create(validated_data) #crée l'utilisateur sans le mot de passe
        if password:
            user.set_password(password) #hachage du mot de passe brut avant de le stocker dans la base de données
            user.save() #sauvegarde l'utilisateur avec le mot de passe haché
        return user
    
    def validate_username(self, value):
        if Utilisateur.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe déjà.")
        return value