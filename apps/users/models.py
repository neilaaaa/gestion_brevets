from django.db import models
from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
    date_ajout = models.DateField(auto_now_add=True, null=True, blank=True)

    @property
    def mdp(self):
        return self.password

    @mdp.setter
    def mdp(self, raw_password):
        self.set_password(raw_password)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username
