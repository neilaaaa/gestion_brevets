from django.db import models
from django.conf import settings

class Recours(models.Model):
    STATUT_CHOICES = [
        ('EN_COURS', 'EN_COURS'),
        ('TRAITE', 'TRAITE'),
        ('REFUSE', 'REFUSE'),
    ]

    id_recours = models.AutoField(primary_key=True)
    date_depot = models.DateField(auto_now_add=True)
    motif = models.CharField(max_length=255)
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_COURS')
    date_traitement = models.DateField(null=True, blank=True)

    # Relations UML
    id_brevet = models.ForeignKey('brevets.Brevet', on_delete=models.CASCADE, db_column='id_brevet')
    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='id')

    def __str__(self):
        return f"Recours {self.id_recours} - {self.motif}"
