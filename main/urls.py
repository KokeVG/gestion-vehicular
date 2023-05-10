from django.urls import path
from . import views
urlpatterns = [
    path("inicio/", views.inicio, name="inicio"),

    path("departamentos/", views.verDepartamentos, name="ver_departamentos"),
    path("departamentos/agregar/", views.agregarDepartamento, name="agregar_departamento"),
    path("departamentos/eliminar/<int:dep_id>/", views.eliminarDepartamento, name="eliminar_departamento"),
    path("departamentos/editar/<int:dep_id>/", views.editarDepartamento, name="editar_departamento"),

    path("vehiculos/", views.verVehiculos, name="ver_vehiculos"),
    path("vehiculos/agregar/", views.agregarVehiculo, name="agregar_vehiculo"),
    path("vehiculos/eliminar/<int:veh_id>/", views.eliminarVehiculo, name="eliminar_vehiculo"),
    path("vehiculos/editar/<int:veh_id>/", views.editarVehiculo, name="editar_vehiculo"),

    path("estacionamientos/", views.verEstacionamientos, name="ver_estacionamientos"),
    path("estacionamientos/agregar/", views.agregarEstacionamiento, name="agregar_estacionamiento"),
    path("estacionamientos/eliminar/<int:est_id>/", views.eliminarEstacionamiento, name="eliminar_estacionamiento"),
    path("estacionamientos/editar/<int:est_id>/", views.editarEstacionamiento, name="editar_estacionamiento"),

    path("ingresos_salidas/", views.ingresosSalidas, name="ingresos_salidas"),
    path("estacionados/", views.estacionados, name="estacionados"),

    path('api/estacionados/', views.EstacionamientosDetailView.as_view(), name="estacionamiento_detail"),
    path('api/ingresossalidas/', views.IngresoSalidaPost.as_view())
]
