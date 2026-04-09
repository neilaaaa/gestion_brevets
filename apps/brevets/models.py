from django.db import models
from django.conf import settings

# --- DemandeBrevet (Must be above classes that reference it) ---
class DemandeBrevet(models.Model):
    STATUT_CHOICES = [('valider', 'valider'), ('non_valider', 'non_valider')]

    id_demande = models.AutoField(primary_key=True)
    titre = models.TextField()
    nature = models.CharField(max_length=100)
    num_depo = models.IntegerField()
    date_depo = models.DateField()
    pays_origine = models.CharField(max_length=100)
    numdemande_CA = models.IntegerField()
    date_CA = models.DateField()
    mandataire = models.CharField(max_length=255)
    date_pouvoir = models.DateField()
    prepose_reception = models.CharField(max_length=255)
    lieu_reception = models.CharField(max_length=255)
    date_reception = models.DateField()
    autre_info = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='non_valider')

    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='id', related_name='demandes')

    def __str__(self):
        return f"{self.id_demande} - {self.titre}"

# --- Deposant ---
class Deposant(models.Model):
    id_dep = models.AutoField(primary_key=True)
    nom_dep = models.CharField(max_length=100)
    prenom_dep = models.CharField(max_length=100)
    denomination = models.CharField(max_length=255)
    adresse_dep = models.CharField(max_length=255)
    nationalite = models.CharField(max_length=100)
    
    id_demande = models.ForeignKey(DemandeBrevet, on_delete=models.CASCADE, db_column='id_demande') #foreignKey au lieu de OnetoOne

    def __str__(self):
        return f"{self.nom_dep} {self.prenom_dep}"

# --- Inventeur ---
class Inventeur(models.Model):
    id_inv = models.AutoField(primary_key=True)
    nom_inv = models.CharField(max_length=100)
    prenom_inv = models.CharField(max_length=100)
    adress_inv = models.CharField(max_length=255)

    id_demande = models.ManyToManyField(DemandeBrevet, related_name='inventeurs') #manyToManyField au lieu de ForeignKey

    def __str__(self):
        return f"{self.nom_inv} {self.prenom_inv}"

# --- Brevet ---
class Brevet(models.Model):
    STATUT_CHOICES = [
        ('ACCEPTER', 'ACCEPTER'),
        ('REFUSER', 'REFUSER'),
        ('EN_ATTENTE', 'EN_ATTENTE'),
    ]

    id_brevet = models.AutoField(primary_key=True)
    num_brevet = models.IntegerField()
    titre = models.CharField(max_length=1000)
    num_depo = models.IntegerField()
    date_depo = models.DateField()
    date_sortie = models.DateField()
    titulaire = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)

    id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='id', related_name='brevets_crees')
    id_demande = models.OneToOneField(DemandeBrevet, on_delete=models.CASCADE, null=True, blank=True, db_column='id_demande')

    def __str__(self):
        return self.titre