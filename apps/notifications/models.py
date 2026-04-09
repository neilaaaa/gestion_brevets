from django.db import models
from django.conf import settings

class Notifications(models.Model):     # UML box exactly named 'Notifications'
    id_notif = models.AutoField( primary_key=True)
    date_notif = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    etat = models.BooleanField(default=False)

    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='id')

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_notif']

    def __str__(self):
        return f"Notif {self.id_notif}"
