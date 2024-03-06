from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from .forms import CustomLoginForm



# Create your views here.
class CustomLoginView(LoginView, View):
    template_name = 'login_acceso.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')
    
    def get(self, request, *args: str, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'home.html')

        return super().get(request, *args, **kwargs)
      
        