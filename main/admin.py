from django.contrib import admin
from .models import Departamento, Estacionamiento, IngresoSalida, Vehiculo

# Register your models here.

admin.site.register(Departamento)
admin.site.register(Estacionamiento)
admin.site.register(Vehiculo)
admin.site.register(IngresoSalida)
