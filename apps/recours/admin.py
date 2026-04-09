from django.contrib import admin
from .models import Recours

@admin.register(Recours)
class RecoursAdmin(admin.ModelAdmin):
    list_display = ('id_recours', 'date_depot', 'motif', 'statut', 'date_traitement', 'id_brevet')
    list_filter = ('statut', 'date_depot')
    search_fields = ('motif', 'id_recours')
