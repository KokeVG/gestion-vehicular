from django.shortcuts import redirect, render
from .models import Estacionados, Estacionamiento, Departamento, IngresoSalida, Vehiculo
from .forms import DepartamentoForm, VehiculoForm, EstacionamientoForm
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from django.db import connection

from django.contrib import messages



TZ=0 #timezone -3

# Create your views here.
def inicio(request):
    context = None
    return render(request,'inicio.html', context)

def estacionados(request):
    estacionados = Estacionados.objects.all().order_by('-fecha_ingreso')
    for e in estacionados:
        e.fecha_ingreso -= datetime.timedelta(hours=TZ)
        e.fecha_salida -= datetime.timedelta(hours=TZ)
    context = {'estacionados':estacionados}
    return render(request,'estacionados.html', context)

def ingresosSalidas(request):
    flujos = IngresoSalida.objects.all().order_by('-fecha_ingreso')
    for f in flujos:
        f.fecha_ingreso -= datetime.timedelta(hours=TZ)
        f.fecha_salida -= datetime.timedelta(hours=TZ)
    context = {'flujos':flujos}
    return render(request,'ingresos_salidas.html', context)

def verDepartamentos(request):
    deps = Departamento.objects.all()
    for d in deps:
        d.fecha_creado -= datetime.timedelta(hours=TZ)
        d.fecha_modificado -= datetime.timedelta(hours=TZ)
    context = {'deps':deps}
    return render(request,'departamentos/ver.html', context)

def agregarDepartamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_departamentos')
    else:
        form = DepartamentoForm()
    context = {'form':form}
    return render(request,'departamentos/agregar.html', context)

def eliminarDepartamento(request, dep_id):
    dep = Departamento.objects.get(id_departamento=dep_id)
    dep.delete()
    return redirect('ver_departamentos')

def editarDepartamento(request, dep_id):
    dep = Departamento.objects.get(id_departamento=dep_id)
    if request.method == "POST":
        form = DepartamentoForm(request.POST, instance=dep)
        if form.is_valid():
            form.save()
            return redirect("ver_departamentos")
    else:
        form = DepartamentoForm(instance=dep)
    context = {"form": form}
    return render(request, "departamentos/editar.html", context)

#Vehículos
def verVehiculos(request):
    vehs = Vehiculo.objects.all()
    for v in vehs:
        v.fecha_creado -= datetime.timedelta(hours=TZ)
        v.fecha_modificado -= datetime.timedelta(hours=TZ)
    context = {'vehs':vehs}
    return render(request,'vehiculos/ver.html', context)

def agregarVehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_vehiculos')
    else:
        form = VehiculoForm()
    context = {'form':form}
    return render(request,'vehiculos/agregar.html', context)

def eliminarVehiculo(request, veh_id):
    veh = Vehiculo.objects.get(id_vehiculo=veh_id)
    veh.delete()
    return redirect('ver_vehiculos')

def editarVehiculo(request, veh_id):
    veh = Vehiculo.objects.get(id_vehiculo=veh_id)
    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=veh)
        if form.is_valid():
            form.save()
            return redirect("ver_vehiculos")
    else:
        form = VehiculoForm(instance=veh)
    context = {"form": form}
    return render(request, "vehiculos/editar.html", context)

#Estacionamientos
def verEstacionamientos(request):
    ests = Estacionamiento.objects.all()
    for e in ests:
        e.fecha_creado -= datetime.timedelta(hours=TZ)
        e.fecha_modificado -= datetime.timedelta(hours=TZ)
    context = {'ests':ests}
    return render(request,'estacionamientos/ver.html', context)

def agregarEstacionamiento(request):
    if request.method == 'POST':
        form = EstacionamientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_estacionamientos')
    else:
        form = EstacionamientoForm()
    context = {'form':form}
    return render(request,'estacionamientos/agregar.html', context)

def eliminarEstacionamiento(request, est_id):
    est = Estacionamiento.objects.get(id_estacionamiento=est_id)
    est.delete()
    return redirect('ver_estacionamientos')

def editarEstacionamiento(request, est_id):
    est = Estacionamiento.objects.get(id_estacionamiento=est_id)
    if request.method == "POST":
        form = EstacionamientoForm(request.POST, instance=est)
        if form.is_valid():
            form.save()
            return redirect("ver_estacionamientos")
    else:
        form = EstacionamientoForm(instance=est)
    context = {"form": form}
    return render(request, "estacionamientos/editar.html", context)


class EstacionamientosDetailView(View):
    def sql(self, id):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM (
                    SELECT e.id_estacionamiento, e.estacionamiento, e.estado, DATE_FORMAT(DATE_SUB(e.fecha_modificado, INTERVAL ''' + str(TZ) + ''' HOUR), "%d-%m-%Y")
                    fecha, DATE_FORMAT(DATE_SUB(e.fecha_modificado, INTERVAL ''' + str(TZ) + ''' HOUR), "%H:%i:%S") hora, v.patente, e.patente_uso
                    FROM main_estacionamiento e
                    LEFT JOIN main_vehiculo v
                    ON e.id_vehiculo_id = v.id_vehiculo) q
                    WHERE q.estacionamiento = ''' + str(id))
            row = cursor.fetchone()
        return row

    def get(self, request):
        x = self.sql(id = request.GET['estacionamiento'])
        dic = {'id_estacionamiento': x[0], 'estacionamiento': x[1], 'estado': x[2], 'fecha': x[3], 'hora': x[4], 'patente': x[5], 'patente_uso': x[6]}
        return JsonResponse(dic, safe=False)

class IngresoSalidaPost(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        #print(request.body)
        jd = json.loads(request.body)
        if jd['tipo'] == 'ingreso':
            #buscar patente
            x = Vehiculo.objects.filter(patente__contains=jd['patente'])
            if x.__len__() != 0:
                IngresoSalida.objects.create(patente=jd['patente'], inscrito='Si', estado='Ingreso')
            else:
                IngresoSalida.objects.create(patente=jd['patente'], inscrito='No', estado='Ingreso')
            datos = {'message': "exito"}
            context = { 'mensaje':  'Vehículo que ingreso no esta inscrito.'}
            return JsonResponse(datos), render(request,'inicio.html', context)
        elif jd['tipo'] == 'salida':
            # verificar que exista un ingreso con la patente que no tenga salida
            lista = IngresoSalida.objects.filter(patente__contains=jd['patente']).order_by('-fecha_ingreso')
            if len(lista)>0:
                x=lista[0]
                update = IngresoSalida.objects.get(id=x.id)
                update.estado = "Salio"
                update.save()
                datos = {'message': "exito"}
            else:
                datos = {'message': "No se encontro el ingreso."}
            return JsonResponse(datos)
        datos = {'message': "error"}
        return JsonResponse(datos)

