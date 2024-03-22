from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
 


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)



class UserRegisterForm(UserCreationForm):
    
    # email = forms.EmailField(required=True, help_text="Debe incluir un signo @ en la dirección de correo electrónico.")
    permiso_gestion_afiliados = forms.BooleanField(required=False)
    permiso_gestion_cursos = forms.BooleanField(required=False)
    permiso_gestion_salon = forms.BooleanField(required=False)
    permiso_gestion_usuarios = forms.BooleanField(required=False)

    class Meta:
        model = User  
        fields = UserCreationForm.Meta.fields + ('email',)

 
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre existente, ingrese uno distinto")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print("asdasd")
        # Validar que el correo electrónico sea único
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, elige otro.")
        
        # Validar que el correo electrónico incluya un signo @
        if '@' not in email:
            raise forms.ValidationError("El correo electrónico debe incluir un signo @.")
        
        return email
    


    


    
    
    