from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Utilisateur


class UtilisateurSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = Utilisateur
        fields = ('id', 'username', 'email', 'password', 'date_ajout', 'groups')
        read_only_fields = ('date_ajout',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        password = validated_data.pop('password', None)

        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        if groups:
            user.groups.set(groups)

        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if groups is not None:
            instance.groups.set(groups)

        return instance

    def validate_username(self, value):
        queryset = Utilisateur.objects.filter(username=value)

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe deja.")

        return value
