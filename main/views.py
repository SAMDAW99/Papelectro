import json
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import *
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from .forms import *
from django.views.generic import *
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
import os
from django.db import transaction
from django.db.models import Q
import mimetypes


class HomePageView(TemplateView):
    template_name = 'main/home.html'


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'main/login.html'

    def get_success_url(self):
        # Redirecciona al dashboard adecuado según el rol del usuario
        return reverse_lazy('file_manager')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/user_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return super().dispatch(request, *args, **kwargs)


class PricingView(ListView):
    model = SubscriptionPlan
    template_name = 'main/pricing.html'
    context_object_name = 'plans'

    def get_queryset(self):
        """Exclude plans the user is already subscribed to or lower plans."""
        user = self.request.user
        if user.is_authenticated:
            try:
                # Get the user's current subscription level
                current_subscription = Subscription.objects.get(user=user)
                # Exclude plans already subscribed to or below the current one
                return SubscriptionPlan.objects.filter(order__gt=current_subscription.plan.order)
            except Subscription.DoesNotExist:
                # If the user has no subscription, show all plans
                return SubscriptionPlan.objects.all()
        return SubscriptionPlan.objects.all()

class ContactView(View):
    template_name = "main/contacto.html"

    def get(self, request, *args, **kwargs):
        # Render the email form
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Extract data from the POST request
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        recipient = "izer094@iesmartinezm.es"  

        # Validate the data
        if not subject or not message or not recipient:
            messages.error(request, "All fields are required.")
            return render(request, self.template_name)

        # Send the email
        try:
            send_mail(
                subject,
                message,
                "izer094@iesmartinezm.es",
                [recipient],
                fail_silently=False,
            )
            messages.success(request, "Email sent successfully!")
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")

        return redirect("gracias_contacto")


class GraciasContactoView(View):
    def get(self, request, *args, **kwargs):
        # Handle GET request (e.g., displaying a thank-you message)
        return render(request, 'main/gracias_contacto.html')

    def post(self, request, *args, **kwargs):
        # Handle POST request if necessary
        return render(request, 'main/gracias_contacto.html')


class ArchivoUploadView(LoginRequiredMixin, CreateView):
    model = Archivo
    template_name = 'main/subir_archivo.html'
    fields = ['archivo', 'nombre']

    def form_valid(self, form):
        # Start a transaction to ensure data consistency
        with transaction.atomic():
            # Get the current directory from URL arguments
            directorio_actual_pk = self.kwargs.get('directorio_pk', None)
            form.instance.propietario = self.request.user  # Set the file owner

            # If there's a directory specified, assign it to the file
            if directorio_actual_pk:
                directorio_actual = get_object_or_404(Directorio, pk=directorio_actual_pk)
                form.instance.directorio = directorio_actual

            # Automatically assign the user's group to the file
            user_group = self.request.user.groups.first()  # Get the first group the user belongs to
            default_group = Group.objects.get(name='DefaultGroup')  # Example default group
            form.instance.grupo = user_group if user_group else default_group


            return super().form_valid(form)

    def get_success_url(self):
        directorio_actual_pk = self.kwargs.get('directorio_pk', None)
        if directorio_actual_pk:
            # If there's a current directory, redirect to it
            return reverse('directorios', kwargs={'directorio_pk': directorio_actual_pk})
        # If there's no directory, redirect to the file manager
        return reverse('file_manager')


class FileManagerView(ListView):
    model = Archivo
    template_name = "main/file_manager.html"
    context_object_name = "archivos"  # Mostrar lista de archivos

    def get_queryset(self):
        """
        Filtra archivos y directorios basados en la jerarquía, búsqueda básica y filtros avanzados.
        """
        # Obtener parámetros básicos y avanzados
        search_query = self.request.GET.get('search', '')
        tipo_archivo = self.request.GET.get('tipo', '')  # Tipo de archivo para el filtro avanzado
        fecha_inicio = self.request.GET.get('fecha_inicio', '')
        fecha_fin = self.request.GET.get('fecha_fin', '')
        directorio_actual = self.kwargs.get('directorio_pk', None)

        # Filtrar archivos y directorios del usuario
        archivos = Archivo.objects.filter(propietario=self.request.user)
        directorios = Directorio.objects.filter(propietario=self.request.user)

        if directorio_actual:
            # Filtrar por el directorio actual
            archivos = archivos.filter(directorio_id=directorio_actual)
            directorios = directorios.filter(parent_id=directorio_actual)
        else:
            # Mostrar archivos y directorios en la raíz
            archivos = archivos.filter(directorio__isnull=True)
            directorios = directorios.filter(parent__isnull=True)

        # Filtro de búsqueda básica
        if search_query:
            archivos = archivos.filter(nombre__icontains=search_query)
            directorios = directorios.filter(nombre__icontains=search_query)

        # Filtro avanzado: tipo de archivo
        if tipo_archivo:
            if tipo_archivo == 'documento':
                archivos = archivos.filter(Q(archivo__icontains='.pdf') | Q(archivo__icontains='.txt'))
            elif tipo_archivo == 'image':
                archivos = archivos.filter(
                    Q(archivo__icontains='.jpg') | Q(archivo__icontains='.jpeg') |
                    Q(archivo__icontains='.png') | Q(archivo__icontains='.gif')
                )     
            elif tipo_archivo == 'video':
                archivos = archivos.filter(
                    Q(archivo__icontains='.mp4') | Q(archivo__icontains='.ogg') |
                    Q(archivo__icontains='.webm'))
            elif tipo_archivo == 'text':
                archivos = archivos.filter(
                    Q(archivo__icontains='.txt') | Q(archivo__icontains='.log') |
                    Q(archivo__icontains='.docx') 
                )   
            elif tipo_archivo == 'pdf':
                archivos = archivos.filter(archivo__icontains='.pdf')

        # Filtro avanzado: rango de fechas
        if fecha_inicio:
            archivos = archivos.filter(fecha_creacion__gte=fecha_inicio)
        if fecha_fin:
            archivos = archivos.filter(fecha_creacion__lte=fecha_fin)

        return archivos, directorios

    def get_context_data(self, **kwargs):
        """
        Añade información de contexto para el renderizado.
        """
        context = super().get_context_data(**kwargs)
        directorio_actual = self.kwargs.get('directorio_pk', None)

        # Obtener archivos y directorios del método get_queryset
        archivos, directorios = self.get_queryset()

        # Manejo de jerarquía actual
        if directorio_actual:
            directorio_actual_obj = get_object_or_404(Directorio, pk=directorio_actual, propietario=self.request.user)
            context['directorio_actual'] = directorio_actual_obj
            context['parent_directorio'] = directorio_actual_obj.parent
        else:
            context['directorio_actual'] = None

        context['archivos'] = archivos
        context['directorios'] = directorios

        # Parámetros para el filtro avanzado
        context['search_query'] = self.request.GET.get('search', '')
        context['tipo_archivo'] = self.request.GET.get('tipo', '')
        context['fecha_inicio'] = self.request.GET.get('fecha_inicio', '')
        context['fecha_fin'] = self.request.GET.get('fecha_fin', '')

        return context







class ArchivoDetailView(LoginRequiredMixin, DetailView):
    model = Archivo
    template_name = "main/detalle_archivo.html"
    context_object_name = "archivo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archivo = self.get_object()
        context['archivo_url'] = archivo.archivo.url 
        return context




class ArchivoDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Obtener el archivo de la base de datos
        archivo = get_object_or_404(Archivo, pk=pk, propietario=request.user)

        # Asegurarse de que el archivo existe
        file_path = archivo.archivo.path
        
        if os.path.exists(file_path):  # Verifica si el archivo realmente existe en el sistema de archivos
            # Determinar el MIME type del archivo
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'  # Default MIME type for binary files
            
            # Establecer el nombre del archivo con la extensión correcta
            filename = archivo.nombre
            
            if '.' not in filename:  # Ensure filename includes extension
                extension = os.path.splitext(archivo.archivo.name)[1]
                filename += extension
            
            # Establecer el encabezado Content-Disposition para que el archivo se descargue
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
            response['Content-Type'] = mime_type
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Retornar la respuesta del archivo
            return response
        
        # Si no se encuentra el archivo o no pertenece al usuario
        messages.error(self.request, "El archivo no está disponible o no tienes permiso para acceder a él.")
        return redirect('file_manager')




class ArchivoDeleteView(LoginRequiredMixin, DeleteView):
    model = Archivo
    context_object_name = 'archivo'
    success_url = reverse_lazy('file_manager')  # Redirect after deletion

    def get_queryset(self):
        # Ensure the user can only delete their own files
        return Archivo.objects.filter(propietario=self.request.user)



            
class ExportPdfView(View):
    def get(self, request, *args, **kwargs):
        # Get the primary key of the file to export
        objkey = self.kwargs.get('pk', None)

        # Get the Archivo object and ensure it has a .pdf extension
        archivo = get_object_or_404(Archivo, pk=objkey)

        if not archivo.archivo.name.endswith('.pdf'):
            # Raise a 404 if the file is not a PDF
            raise Http404("The requested file is not a PDF.")

        # Build the full path to the file
        file_path = os.path.join(settings.MEDIA_ROOT, archivo.archivo.name)

        try:
            # Return the file as a response
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404("File not found.")
        


class DirectorioCreateView(LoginRequiredMixin, CreateView):
    model = Directorio
    template_name = 'main/crear_directorio.html'
    fields = ['nombre']  # Add more fields if needed

    def form_valid(self, form):
        # Start a transaction to ensure data consistency
        with transaction.atomic():
            directorio_actual_pk = self.kwargs.get('directorio_pk', None)
            form.instance.propietario = self.request.user  # Set the directory owner

            if directorio_actual_pk:
                # If there is a parent directory, assign it
                directorio_padre = get_object_or_404(Directorio, pk=directorio_actual_pk)
                form.instance.parent = directorio_padre

            return super().form_valid(form)

    def get_success_url(self):
        directorio_actual_pk = self.kwargs.get('directorio_pk', None)
        if directorio_actual_pk:
            # Redirect to the current directory
            return reverse('directorios', kwargs={'directorio_pk': directorio_actual_pk})
        # Redirect to the main file manager if there's no parent directory
        return reverse('file_manager')
  



class DirectorioDeleteView(DeleteView):
    model = Directorio
    success_url = reverse_lazy('file_manager')
    
    

# class MoverArchivoView(View):
#     def post(self, request, *args, **kwargs):
#         archivo_id = kwargs.get('pk')
#         data = json.loads(request.body)
#         directorio_id = data.get('folderId')

#         # Start a transaction to ensure data consistency
#         with transaction.atomic():
#             archivo = get_object_or_404(Archivo, pk=archivo_id, propietario=request.user)
#             directorio = get_object_or_404(Directorio, pk=directorio_id, propietario=request.user)

#             # Move the file to the new directory
#             archivo.directorio = directorio
#             archivo.save()
        
#         # Return success response
#         return JsonResponse({'status': 'success'})




class RegisterPlanView(CreateView):
    template_name = 'main/register_plan.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('pricing')  # Redirect after successful registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the first plan and add it to the context
        plan = SubscriptionPlan.objects.first()
        if plan:
            context['plan'] = plan
        else:
            messages.warning(self.request, "No subscription plans found.")
        return context

    def form_valid(self, form):
        # Save the user
        user = form.save(commit=False)
        user.is_superuser = True 
        user.is_staff = True      
        user.save()

        # Add user-specific logic (e.g., associating a plan)
        plan = SubscriptionPlan.objects.first()
        if plan:
            messages.success(self.request, f"User {user.username} registered for the {plan.name} plan!")
        else:
            messages.warning(self.request, f"User {user.username} registered, but no plan is associated.")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please correct the errors below.")
        return super().form_invalid(form)
    
class CreateGroupView(CreateView):
    model = Group
    template_name = 'create_group.html'
    fields = ['name']
    success_url = reverse_lazy('manage_groups')