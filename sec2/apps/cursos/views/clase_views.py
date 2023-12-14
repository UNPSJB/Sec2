from ..models import Clase
from ..forms.clase_forms import *
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.shortcuts import redirect
from sec2.utils import ListFilterView

##--------------- CREACION DE CLASE --------------------------------
class ClaseCreateView(CreateView):
    model = Clase
    form_class = ClaseForm
    template_name = 'clase/clase_form.html'
    success_url = None  # Asigna un valor predeterminado a success_url

    def get_initial(self,*args, **kwargs):
        dictado= Dictado.objects.get(pk=self.kwargs.get("pk"))
        return {'dictado':dictado}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictado = Dictado.objects.get(id = self.kwargs.get('pk'))
        context['dictado'] = dictado
        context['titulo'] = f"Alta de clase para el dictado {dictado.cantidad_clase}"
        tiene_aula = Aula.objects.exists()
        context['tiene_aula'] = tiene_aula
        return context

    def get(self, request, *args, **kwargs):
        # Verificar si hay alguna actividad antes de renderizar el formulario
        if Aula.objects.exists():
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'clase/falta_aula.html', {'titulo': 'Te falta menos calle'})

    def post(self, request, *args, **kwargs):
        form = ClaseForm(request.POST)
        dictado_id = kwargs.get("pk")
        dictado = Dictado.objects.get(pk=dictado_id)

        if form.is_valid():
            form.save(dictado)

            # Redirige a la vista DictadoDetailView con el pk del dictado
            return redirect('cursos:dictado', pk=dictado_id)
        else:
            context = {'form': form, 'dictado_id': dictado_id, 'titulo': f"Alta de clase para el dictado {dictado.cantidad_clase}"}
            return render(request, self.template_name, context)


    def get_success_url(self):
        # La redirección se maneja en el método post, por lo que este método puede retornar cualquier cosa (por ejemplo, None)
        return None
    
    def form_valid(self, form):
        dictado_id = self.kwargs.get('pk')
        dictado = Dictado.objects.get(pk=dictado_id)
        form.save(dictado)
        return super().form_valid(form)


class ClaseListView(ListFilterView):
    model = Clase
    paginate_by = 100
    filter_class = ClaseFilterForm
