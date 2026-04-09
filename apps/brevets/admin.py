from django.contrib import admin
from .models import Deposant, Inventeur, DemandeBrevet, Brevet

# --- Inline pour Deposant ---
class DeposantInline(admin.StackedInline):
    model = Deposant
    extra = 0
    can_delete = False

# --- Inline pour Inventeur ---
class InventeurInline(admin.TabularInline):
    model = Inventeur.id_demande.through  # table intermédiaire ManyToMany
    extra = 1
    verbose_name = "Inventeur"
    verbose_name_plural = "Inventeurs"

# --- Admin Deposant ---
@admin.register(Deposant)
class DeposantAdmin(admin.ModelAdmin):
    list_display = ('id_dep', 'nom_dep', 'prenom_dep', 'denomination', 'nationalite', 'id_demande')
    search_fields = ('nom_dep', 'denomination', 'id_dep')
    list_filter = ('nationalite',)

# --- Admin Inventeur ---
@admin.register(Inventeur)
class InventeurAdmin(admin.ModelAdmin):
    list_display = ('id_inv', 'nom_inv', 'prenom_inv', 'get_demandes')
    search_fields = ('nom_inv', 'prenom_inv', 'id_inv')
    list_filter = ('id_demande__titre',)

    @admin.display(description='Demandes')
    def get_demandes(self, obj):
        return ", ".join([str(d.titre) for d in obj.id_demande.all()])

# --- Admin DemandeBrevet ---
@admin.register(DemandeBrevet)
class DemandeBrevetAdmin(admin.ModelAdmin):
    list_display = ('id_demande', 'titre', 'statut', 'num_depo')
    list_filter = ('statut', 'date_depo', 'pays_origine')
    search_fields = ('titre', 'id_demande', 'num_depo')
    inlines = [DeposantInline, InventeurInline]

    fieldsets = (
        ('Identification', {
            'fields': ('titre', 'nature', 'statut')
        }),
        ('Détails du Dépôt', {
            'fields': ('num_depo', 'date_depo', 'pays_origine', 'numdemande_CA', 'date_CA')
        }),
        ('Réception et Mandat', {
            'fields': ('mandataire', 'date_pouvoir', 'prepose_reception', 'lieu_reception', 'date_reception')
        }),
        ('Rattachement Utilisateur', {
            'fields': ('id', 'autre_info')  # id = ForeignKey vers l'utilisateur
        }),
    )

# --- Admin Brevet ---
@admin.register(Brevet)
class BrevetAdmin(admin.ModelAdmin):
    list_display = ('id_brevet', 'num_brevet', 'titre', 'statut', 'date_sortie', 'titulaire', 'id_demande')
    list_filter = ('statut', 'date_sortie')
    search_fields = ('titre', 'id_brevet', 'titulaire')
    