from django.db import models
from django.utils import timezone

# Create your models here.
class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    departamento = models.CharField(max_length=5)
    block = models.CharField(max_length=3)
    fecha_creado =  models.DateTimeField(auto_now_add=True, auto_now=False)
    fecha_modificado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return (str(self.departamento) + " " + self.block)

class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    patente = models.CharField(max_length=10, unique=True)
    rut_propietario = models.CharField(max_length=12, unique=False, null=True)
    fecha_creado =  models.DateTimeField(auto_now_add=True, auto_now=False)
    fecha_modificado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.patente

class Estacionamiento(models.Model):
    id_estacionamiento = models.AutoField(primary_key=True)
    estacionamiento = models.CharField(max_length=10, unique=True, null=True)
    estado = models.CharField(max_length=20, null=True, choices=(('Libre', 'Libre'), ('Ocupado', 'Ocupado'), ('Sin asignar', 'Sin asignar')))
    patente_uso = models.CharField(max_length=10, null=True)
    fecha_creado =  models.DateTimeField(auto_now_add=True, auto_now=False)
    fecha_modificado = models.DateTimeField(auto_now_add=False, auto_now=True)
    id_departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.SET_NULL)
    id_vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.estacionamiento

class IngresoSalida(models.Model):
    id = models.AutoField(primary_key=True)
    patente = models.CharField(max_length=10, null=True)
    inscrito = models.CharField(max_length=2, null=True, choices=(('Si', 'Si'), ('No', 'No')))
    estado = models.CharField(max_length=7, null=True, choices=(('Ingreso', 'Ingreso'), ('Salio', 'Salio')))
    fecha_ingreso =  models.DateTimeField(auto_now_add=True, auto_now=False)
    fecha_salida = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return (str(self.patente) + " " + self.inscrito + " " + self.estado)

class Estacionados(models.Model):
    id = models.AutoField(primary_key=True)
    estacionamiento = models.ForeignKey(Estacionamiento, null=True, on_delete=models.SET_NULL)
    patente = models.CharField(max_length=10)
    estado = models.CharField(max_length=20, null=True, choices=(('Ingreso', 'Ingreso'), ('Salio', 'Salio')))
    fecha_ingreso =  models.DateTimeField(auto_now_add=True, auto_now=False)
    fecha_salida = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return (str(self.patente) + " " + self.estado)