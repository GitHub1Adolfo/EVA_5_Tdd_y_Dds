from django.contrib.auth.models import AbstractUser
from django.db import models
from sucursales.models import Sucursal

class Usuario(AbstractUser):
    ROLES = [
        ('administrador', 'Administrador'),
        ('vendedor', 'Vendedor'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"