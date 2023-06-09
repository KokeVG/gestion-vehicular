# Generated by Django 3.2.9 on 2021-12-08 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20211208_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estacionados',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vehiculo', models.CharField(max_length=10)),
                ('estado', models.CharField(choices=[('Ingreso', 'Ingreso'), ('Salio', 'Salio')], max_length=20, null=True)),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True)),
                ('fecha_salida', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='ingresosalida',
            name='estado',
        ),
    ]
