from django.shortcuts import render
from django.http import HttpRequest
from apps.afiliados.forms import FormularioAfiliado


class FormularioAfiliadoView(HttpRequest):

    def index(request):
        afiliado = FormularioAfiliado()
        return render(request,"formularioAfiliado.html", {'form':afiliado})
    
    def procesarFormulario(request):
        afiliado = FormularioAfiliado(request.POST)
        if afiliado.is_valid():
            afiliado.save()
            afiliado = FormularioAfiliado()

        return render(request,"formularioAfiliado.html", {'form':afiliado,'mensaje':'ok'})