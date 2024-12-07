import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import *
from main.models import *
from django.contrib.admin.widgets import FilteredSelectMultiple  

USER_TYPE_CHOICES = [
    ('user', 'User'),
    ('staff', 'Staff'),
    ('admin', 'Admin'),
]

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='User Type'
    )
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        username = cleaned_data.get('username')

        if user_type == 'staff':
            staff_user_exists = User.objects.filter(username=username, is_staff=True).exists()
            if not staff_user_exists:
                raise forms.ValidationError("No estás autorizado para iniciar sesión como personal.")
        
        return cleaned_data


class RegistrarseForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Usuario'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Contraseña'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Repetir contraseña'
    )
  

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")



        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        return user
    
    
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