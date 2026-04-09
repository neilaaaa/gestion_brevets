from django.contrib import admin
from .models import Notifications

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id_notif', 'date_notif', 'etat', 'id')
    list_filter = ('etat', 'date_notif')
    search_fields = ('id_notif', 'message')
