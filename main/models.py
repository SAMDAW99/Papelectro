from django.contrib.auth.models import User
from django.db import models

class Usuario(models.Model):
    # Relación uno a uno con el modelo User de Django
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False)  # Para diferenciar usuarios admin


#   saldo = models.FloatField(max_length=30, default=0)

    def __str__(self):
        return str(self.usuario)

    class Meta:
        verbose_name_plural = "Usuarios"