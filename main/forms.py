import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import *
from main.models import *
from django.contrib.admin.widgets import FilteredSelectMultiple  



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

   


class RegistroConEmpresaForm(UserCreationForm):
    # Campos del usuario
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
        label='Usuario'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir Contraseña'}),
        label='Repetir Contraseña'
    )

    # Campos de la empresa
    nombre_empresa = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Empresa'}),
        label='Nombre de la Empresa'
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción de la Empresa'}),
        label='Descripción',
        required=False
    )
    codigo_empresa = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de Empresa (5 caracteres)'}),
        label='Código de Empresa',
    )
    
    def clean_codigo_empresa(self):
        codigo = self.cleaned_data.get('codigo_empresa')
        if Empresa.objects.filter(codigo_empresa=codigo).exists():
            raise forms.ValidationError("El código de empresa ya está en uso. Por favor, elige otro.")
        return codigo

    def save_user(self, commit=True):
        # Guarda el usuario
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    def save_empresa(self, user, commit=True):
        # Guarda la empresa asociada al usuario
        empresa = Empresa(
            nombre=self.cleaned_data.get('nombre_empresa'),
            descripcion=self.cleaned_data.get('descripcion'),
            codigo_empresa=self.cleaned_data.get('codigo_empresa'),
            ceo=user
        )
        if commit:
            empresa.save()
        return empresa
    
   


    
    
class UserForm(UserChangeForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)


    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
    
    
class TarjetaCreditoForm(forms.ModelForm):
    class Meta:
        model = TarjetaCredito
        fields = ['numero_tarjeta', 'fecha_vencimiento', 'nombre_titular']

    def clean_numero_tarjeta(self):
        numero_tarjeta = self.cleaned_data.get('numero_tarjeta')
        if not numero_tarjeta.isdigit():
            raise forms.ValidationError("El número de tarjeta debe contener solo dígitos.")
        if len(numero_tarjeta) != 16:
            raise forms.ValidationError("El número de tarjeta debe tener 16 dígitos.")
        return numero_tarjeta

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        if fecha_vencimiento < datetime.date.today():
            raise forms.ValidationError("La fecha de vencimiento debe ser una fecha futura.")
        return fecha_vencimiento
    
class CambiarContrasForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CambiarContrasForm, self).__init__(*args, **kwargs)



class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'groups']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'groups': 'Departamento',
        }
        

              
class GroupPermissionsForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['permissions']
        widgets = {
            'permissions': FilteredSelectMultiple('Permisos', is_stacked=False),
        }
        
        
