from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Utilisateur


class GroupNamesField(serializers.Field):
    def to_representation(self, value):
        return list(value.values_list('name', flat=True))

    def to_internal_value(self, data):
        if data is None:
            return []
        if not isinstance(data, list):
            raise serializers.ValidationError("Le role doit etre une liste.")

        normalized = []
        for group_name in data:
            cleaned = str(group_name).strip().lower()
            if cleaned and cleaned not in normalized:
                normalized.append(cleaned)
        return normalized


class UtilisateurSerializer(serializers.ModelSerializer):
    groups = GroupNamesField(required=False)

    class Meta:
        model = Utilisateur
        fields = (
            'id',
            'username',
            'email',
            'password',
            'date_ajout',
            'groups',
            'is_staff',
            'is_superuser',
            'is_active',
        )
        read_only_fields = ('date_ajout',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def _resolve_groups(self, groups):
        resolved = []
        for group_name in groups:
            group = Group.objects.filter(name__iexact=group_name).first()
            if group is None:
                group = Group.objects.create(name=group_name)
            resolved.append(group)
        return resolved

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        password = validated_data.pop('password', None)

        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        if groups:
            user.groups.set(self._resolve_groups(groups))

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
            instance.groups.set(self._resolve_groups(groups))

        return instance

    def validate_username(self, value):
        queryset = Utilisateur.objects.filter(username=value)

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe deja.")

        return value
