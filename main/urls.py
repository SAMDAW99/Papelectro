from main.views import *
from django.urls import path
from django.conf.urls.static import static


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('user_dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('contacto/', ContactView.as_view(), name='contacto'),
    path('gracias_contacto/', GraciasContactoView.as_view(), name='gracias_contacto'),
    path('file_manager/', FileManagerView.as_view(), name="file_manager"),
    path('archivos/descargar/<int:pk>/', ArchivoDownloadView.as_view(), name="archivos-descargar"),
    path('archivo/<int:pk>/borrar/', ArchivoDeleteView.as_view(), name='archivos-borrar'),
    path('archivo/<int:pk>/export-pdf/', ExportPdfView.as_view(), name='export-pdf'),
    path('archivo/<int:pk>/detalle/', ArchivoDetailView.as_view(), name='detalle-archivo'),
    path('directorios/crear/', DirectorioCreateView.as_view(), name='crear-directorio-none'),
    path('directorios/borrar/<int:pk>/', DirectorioDeleteView.as_view(), name='borrar-directorio'),
    # path('archivos/mover/<int:pk>/', MoverArchivoView.as_view(), name='mover-archivo'),
    path('directorios/<int:directorio_pk>/', FileManagerView.as_view(), name="directorios"),
    path('directorios/crear/<int:directorio_pk>/', DirectorioCreateView.as_view(), name='crear-directorio'),
    path('archivos/subir/<int:directorio_pk>/', ArchivoUploadView.as_view(), name='archivos-subir'),
    path('archivos/subir/', ArchivoUploadView.as_view(), name='archivos-subir-none'),
    path("register-plan/", RegisterPlanView.as_view(), name="register_plan"),
    path('perfil_usuario/nueva_tarjeta/', NuevaTarjeta.as_view(), name='nueva_tarjeta'),
    path('perfil_usuario/<int:pk>/editar_tarjeta/', EditarTarjeta.as_view(), name='editar_tarjeta'),
    path('perfil_usuario/<int:pk>/eliminar_tarjeta/', EliminarTarjeta.as_view(), name='eliminar_tarjeta'),
    path('cambiar_contras/', CambiarContras.as_view(), name='cambiar_contras'),
    path('perfil_usuario/editar_usuario/', EditarPerfil.as_view(), name='editar_usuario'),
    path('perfil_usuario/', PerfilUsuario.as_view(), name='perfil_usuario'),
    path('info/', InfoPageView.as_view(), name='info'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
