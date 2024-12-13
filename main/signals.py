from django.dispatch import receiver
from main.models import Usuario, Empresa
from .signal_definition import usuario_creado_signal
from django.db.models.signals import post_save
from django.contrib.auth.models import User



@receiver(usuario_creado_signal)
def crear_usuario_asociado(sender, instance, empresa, **kwargs):
    if instance and empresa:
        Usuario.objects.create(usuario=instance, empresa=empresa)


@receiver(post_save, sender=User)
def asignar_empresa_al_usuario(sender, instance, created, **kwargs):
    """
    Asigna automáticamente la empresa del creador al usuario recién creado.
    """
    if created and hasattr(instance, '_created_by'):
        try:
            # Obtener la empresa del usuario que creó este usuario
            usuario_creador = Usuario.objects.get(usuario=instance._created_by)
            empresa_actual = usuario_creador.empresa
            
            # Crear el objeto Usuario asociado con el nuevo User
            Usuario.objects.create(usuario=instance, empresa=empresa_actual)
        except Usuario.DoesNotExist:
            # Si el creador no tiene una empresa asignada, no se hace nada
            pass