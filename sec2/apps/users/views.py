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


def obtenerPermiso(name):
# Precondicion: {name} Exits in {"administador","cliente","empleadoPublico"}
        
        if name == "gestion_afiliados":
            content_type = ContentType.objects.get_for_model(Afiliado)
            permiso, creado = Permission.objects.get_or_create(
                codename='permission_gestion_afiliado',
                name='Control total afiliado',
                content_type=content_type,
            )
            return permiso
        
        if name == "gestion_cursos":
            content_type = ContentType.objects.get_for_model(Curso)
            permiso, creado = Permission.objects.get_or_create(
                codename='permission_gestion_curso',
                name='Control total curso',
                content_type=content_type,
            )
            return permiso
        
        if name == "gestion_alquileres":
            content_type = ContentType.objects.get_for_model(Alquiler)
            permiso, creado = Permission.objects.get_or_create(
                codename='permission_gestion_alquiler',
                name='Control total alquiler',
                content_type=content_type,
            )
            return permiso
        
        if name == "gestion_usuarios":
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
                user = User.objects.get(username=form.cleaned_data["username"])
                permiso = obtenerPermiso("gestion_afiliados")
                user.user_permissions.add(permiso)
        
        
        if form.cleaned_data['permiso_gestion_cursos'] :
                user = User.objects.get(username=form.cleaned_data["username"])
                permiso = obtenerPermiso("gestion_cursos")
                user.user_permissions.add(permiso)
        

        
        if form.cleaned_data['permiso_gestion_salon'] :
                user = User.objects.get(username=form.cleaned_data["username"])
                permiso = obtenerPermiso("gestion_alquileres")
                user.user_permissions.add(permiso)

        
        if form.cleaned_data['permiso_gestion_usuarios'] :
                user = User.objects.get(username=form.cleaned_data["username"])
                permiso = obtenerPermiso("gestion_usuarios")
                user.user_permissions.add(permiso)

        
        messages.success(self.request, 'Usuario creado exitosamente')
        return redirect('users:user_register')
        
       
    
  
     
    
