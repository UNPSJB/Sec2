from django.contrib import admin

from apps.alquileres.models import Encargado, Salon, Servicio

admin.site.register(Encargado)
admin.site.register(Servicio)
admin.site.register(Salon)