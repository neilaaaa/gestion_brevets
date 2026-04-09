from django.db import models
from django.conf import settings

class Paiement(models.Model):
    STATUT_CHOICES = [
        ('payer', 'payer'),
        ('non_payer', 'non_payer'),
    ]

    id_paiement = models.AutoField(primary_key=True)
    date_paiement = models.DateField()
    montant_total = models.FloatField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='non_payer')

    # Relations UML
    id_brevet = models.OneToOneField('brevets.Brevet', on_delete=models.CASCADE, db_column='id_brevet')
    id_document = models.OneToOneField('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, db_column='id_document')
    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='id')

    def __str__(self):
        return f"Paiement {self.id_paiement}"
