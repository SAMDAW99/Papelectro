from django.contrib.auth.models import User, Group
from django.db import models


class Empresa(models.Model):
    codigo_empresa = models.CharField(max_length=5, unique=True, null= False)
    nombre = models.CharField(max_length=20, unique=True)
    ceo = models.OneToOneField(User, on_delete=models.CASCADE, related_name="empresa_ceo")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo_empresa})"
    
class GrupoPersonalizado(Group):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="grupos")




class Directorio(models.Model):
    nombre = models.CharField(max_length=255)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subdirectorios', on_delete=models.CASCADE)
    favorito = models.BooleanField(default=False)  # New field to mark as favorite

    def __str__(self):
        return self.nombre
    
    
class Archivo(models.Model):
    archivo = models.FileField(upload_to='uploads/')
    nombre = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="archivos")
    directorio = models.ForeignKey(Directorio, null=True, blank=True, related_name='archivos', on_delete=models.CASCADE)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)  # Asociar archivo a un grupo
    favorito = models.BooleanField(default=False)  # New field to mark as favorite

    @property
    def tipo(self):
        if self.archivo.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return 'image'
        elif self.archivo.name.endswith(('.mp4', '.webm', '.ogg')):
            return 'video'
        elif self.archivo.name.endswith('.pdf'):
            return 'pdf'
        elif self.archivo.name.endswith(('.txt', '.md', '.log')):
            return 'text'
        return 'unknown'


class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.usuario)

    class Meta:
        verbose_name_plural = "Usuarios"

        
        
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    features = models.TextField(help_text="Enter features separated by commas.")
    button_class = models.CharField(max_length=50, default="btn-morado")
    order = models.IntegerField()

    def get_features_list(self):
        return [feature.strip() for feature in self.features.split(",")]

    def __str__(self):
        return self.name
 

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"   
    
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo Electrónico")
    subject = models.CharField(max_length=200, verbose_name="Asunto")
    message = models.TextField(verbose_name="Mensaje")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class Documento(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_modificacion = models.DateTimeField(auto_now=True)
    archivo = models.ForeignKey(Archivo, related_name="documentos", on_delete=models.CASCADE)

class Configuracion(models.Model):
    clave = models.CharField(max_length=50, unique=True)
    valor = models.TextField()
    
class TarjetaCredito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_tarjeta = models.CharField(max_length=16)
    nombre_titular = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField(max_length=10)

    def __str__(self):
        return self.numero_tarjeta