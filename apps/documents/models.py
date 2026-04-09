from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# --- TypeDocument ---
class TypeDocument(models.Model):
    id_type = models.AutoField(primary_key=True)
    nom_type = models.CharField(max_length=100)
    description = models.TextField()
    taille_max = models.IntegerField()
    format_autorise = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_type

# --- Document ---
class Document(models.Model):
    id_document = models.AutoField(primary_key=True)
    nom_document = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='documents/') 
    date_ajout = models.DateField(auto_now_add=True)

    # Relations UML
    id_type = models.ForeignKey(TypeDocument, on_delete=models.CASCADE, db_column='id_type')
    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='id')
    id_brevet = models.ForeignKey('brevets.Brevet', on_delete=models.CASCADE, null=True, blank=True, db_column='id_brevet')
    id_demande = models.ForeignKey(
        'brevets.DemandeBrevet',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='id_demande'
    )
    id_paiement = models.OneToOneField('paiements.Paiement', on_delete=models.CASCADE, null=True, blank=True, db_column='id_paiement')
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
    def clean(self):
        if not self.id_demande and not self.id_brevet:
            raise ValidationError("Un document doit être obligatoirement lié à une Demande de Brevet ou à un Brevet.")

    def __str__(self):
        return self.nom_document
