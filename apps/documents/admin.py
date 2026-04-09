from django.contrib import admin
from .models import TypeDocument, Document 

@admin.register(TypeDocument)
class TypeDocumentAdmin(admin.ModelAdmin):
    list_display = ('id_type', 'nom_type', 'taille_max', 'format_autorise')
    search_fields = ('nom_type',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id_document', 'nom_document', 'id_type', 'date_ajout', 'id', 'id_demande', 'id_brevet', 'id_paiement')
    list_filter = ('id_type', 'date_ajout')
    search_fields = ('nom_document', 'id_demande__titre', 'id_brevet__titre')
