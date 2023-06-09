# Generated by Django 3.2.9 on 2022-01-08 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_vehiculo_rut_propietario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacionados',
            name='estacionamiento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.estacionamiento'),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='id_departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.departamento'),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='id_vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.vehiculo'),
        ),
    ]
