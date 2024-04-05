from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from apps.afiliados.models import Afiliado
from apps.alquileres.models import Alquiler
from apps.cursos.models import Curso
from .forms import CustomLoginForm, UserRegisterForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User,Permission
from django.contrib.auth.models import AbstractUser
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


def obtenerPermisoUsuarios():
      content_type = ContentType.objects.get_for_model(User)
      permiso, creado = Permission.objects.get_or_create(
                                                          codename='permission_gestion_usuario',
                                                          name='Control total user',
                                                          content_type=content_type,          
                                                        )
      return permiso
        




class CustomLoginView(LoginView, View):
    template_name = 'login_acceso.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')
    
    def get(self, request, *args: str, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().get(request, *args, **kwargs)


def cerrar_session(request):
    logout(request)
    return redirect('users:login')

class CreacionUsuarios(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'creacion_usuarios.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    login_url = '/login/'
    permission_required = "auth.permission_gestion_usuario"

    
    
    def form_valid(self, form):
        print("entre")

        # Aquí puedes acceder a los datos del formulario
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        
        
        form.save() 
                
        user = User.objects.get(username=username)

        if form.cleaned_data['permiso_gestion_afiliados'] :
                permiso = Permission.objects.get(codename='permission_gestion_afiliado')
                user.user_permissions.add(permiso)
        
        
        if form.cleaned_data['permiso_gestion_cursos'] :
                permiso = Permission.objects.get(codename='permission_gestion_curso')
                user.user_permissions.add(permiso)
        

        
        if form.cleaned_data['permiso_gestion_salon'] :
                permiso = Permission.objects.get(codename='permission_gestion_alquiler')
                user.user_permissions.add(permiso)

        
        if form.cleaned_data['permiso_gestion_usuarios'] :
                permiso = obtenerPermisoUsuarios()
                user.user_permissions.add(permiso)

        user.save()        
        messages.success(self.request, 'Usuario creado exitosamente')
        return redirect('users:user_register')
        
       
    
  
     
    
