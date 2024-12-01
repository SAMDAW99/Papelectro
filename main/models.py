from django.contrib.auth.models import User
from django.db import models


class Directorio(models.Model):
    nombre = models.CharField(max_length=255)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subdirectorios', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    
class Archivo(models.Model):
    archivo = models.FileField(upload_to='uploads/')
    nombre = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    directorio = models.ForeignKey(Directorio, null=True, blank=True, related_name='archivos', on_delete=models.CASCADE)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)

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
    # Relación uno a uno con el modelo User de Django
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False)  # Para diferenciar usuarios admin
    

    def __str__(self):
        return str(self.usuario)

    class Meta:
        verbose_name_plural = "Usuarios"
        
        
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    features = models.TextField(help_text="Enter features separated by commas.")
    button_class = models.CharField(max_length=50, default="btn-primary")
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