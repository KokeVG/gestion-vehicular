from django import forms
#from django.forms.widgets import Textarea
from .models import Departamento, Vehiculo, Estacionamiento

class DepartamentoForm(forms.ModelForm):
    
    class Meta:
        model = Departamento
        fields = ['departamento', 'block']

class VehiculoForm(forms.ModelForm):
    
    class Meta:
        model = Vehiculo
        fields = ['patente', 'rut_propietario']

class EstacionamientoForm(forms.ModelForm):
    
    class Meta:
        model = Estacionamiento
        fields = ['id_departamento', 'estacionamiento', 'id_vehiculo', 'estado']