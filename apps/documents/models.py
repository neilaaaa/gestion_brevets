from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Document(models.Model):
    TYPE_CHOICES = [
        ("brevet",   "Brevet"),
        ("Memoire Descriptif", "memoire descriptif"),
        ("demande",  "Demande"),
        ("recours",  "Recours"),
        ("paiement", "Paiement"),
        ("autre", "Autre"),
        ("autre_type", "Autre Type")
        ]
    id_document = models.AutoField(primary_key=True)
    nom_document = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    fichier = models.FileField(upload_to='documents/')
    date_ajout = models.DateField( null=True, blank=True)
    date_sortie_officielle = models.DateField( null=True, blank=True)

    type_document = models.CharField( 
        max_length=50,
        choices=TYPE_CHOICES,
        default="brevet"
    )
    autre_type = models.CharField(max_length=100, blank=True, default="")
    
    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='id')
    id_brevet = models.ForeignKey('brevets.Brevet', on_delete=models.CASCADE, null=True, blank=True, db_column='id_brevet')
    id_demande = models.ForeignKey(
        'brevets.DemandeBrevet',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='id_demande'
    )
    id_paiement = models.OneToOneField(
        'paiements.Paiement',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='id_paiement'
    )

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def clean(self):
        if not self.id_demande and not self.id_brevet:
            raise ValidationError(
                "Un document doit etre obligatoirement lie a une Demande de Brevet ou a un Brevet."
            )

    def __str__(self):
        return self.nom_document
