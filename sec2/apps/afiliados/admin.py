from django.contrib import admin

from .models import Afiliado, Familiar
from apps.personas.models import Rol

#Register your models here.

admin.site.register(Familiar)
admin.site.register(Afiliado)
admin.site.register(Rol)