# Generated by Django 5.1.3 on 2025-02-07 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constructor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('foto', models.FileField(blank=True, null=True, upload_to='constructores')),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObraPublica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('ubicacion', models.CharField(blank=True, max_length=200, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('planeacion', 'Planeación'), ('en_proceso', 'En Proceso'), ('finalizada', 'Finalizada'), ('cancelada', 'Cancelada')], default='planeacion', max_length=50)),
                ('constructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='obras', to='obras.constructor')),
            ],
        ),
        migrations.CreateModel(
            name='FechaInicio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fechas_inicio', to='obras.obrapublica')),
            ],
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('presupuesto', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Monto Aprobado')),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presupuestos', to='obras.obrapublica')),
            ],
        ),
    ]
