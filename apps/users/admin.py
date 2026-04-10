from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'get_groups', 'is_staff', 'date_ajout')
    list_filter = ('groups', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

    fieldsets = (
        ('Credentials (UML: username, mdp)', {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'date_ajout')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'groups'),
        }),
    )

    readonly_fields = ('date_ajout',)

    @admin.display(description='Groupes')
    def get_groups(self, obj):
        return ", ".join(obj.groups.values_list('name', flat=True))
