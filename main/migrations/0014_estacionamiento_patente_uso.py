# Generated by Django 3.2.9 on 2021-12-29 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_ingresosalida_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='estacionamiento',
            name='patente_uso',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
