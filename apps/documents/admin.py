from django.contrib import admin
from .models import Document 


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id_document', 'nom_document', 'type_document', 'date_ajout', 'id', 'id_demande', 'id_brevet', 'id_paiement')
    list_filter = ('type_document', 'date_ajout')
    search_fields = ('nom_document', 'id_demande__titre', 'id_brevet__titre')
    ordering = ('-date_ajout',)
