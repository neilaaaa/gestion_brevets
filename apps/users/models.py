from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    id_role = models.AutoField(primary_key=True)
    nom_role = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"

    def __str__(self):
        return self.nom_role

class Utilisateur(AbstractUser):
    date_ajout = models.DateField(auto_now_add=True, null=True, blank=True)
    
    # Propriété pour supporter l'alias "mdp" figurant sur le diagramme UML
    @property
    def mdp(self):
        return self.password #mot de passe haché stocké dans la base de données exemple: pbkdf2_sha256$39..
        
    @mdp.setter
    def mdp(self, raw_password):
        self.set_password(raw_password) #mot de passe brut exemple:'1234'

    id_role = models.ForeignKey(Role, on_delete=models.PROTECT, db_column='id_role', null=True, blank=True)
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username