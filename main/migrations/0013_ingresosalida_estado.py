# Generated by Django 3.2.9 on 2021-12-10 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20211210_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingresosalida',
            name='estado',
            field=models.CharField(choices=[('Ingreso', 'Ingreso'), ('Salio', 'Salio')], max_length=7, null=True),
        ),
    ]
