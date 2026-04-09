from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('id_paiement', 'date_paiement', 'montant_total', 'statut', 'id_brevet', 'id_document')
    list_filter = ('statut', 'date_paiement')
    search_fields = ('id_paiement',)
