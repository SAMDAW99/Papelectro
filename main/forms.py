from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

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
