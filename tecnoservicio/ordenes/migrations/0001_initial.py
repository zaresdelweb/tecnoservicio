# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('folio', models.PositiveIntegerField(unique=True)),
                ('fecha_alta', models.DateTimeField(auto_now_add=True)),
                ('estatus', models.CharField(max_length=30, choices=[(b'Nueva', b'Nueva'), (b'Alerta', b'Alerta'), (b'Espera de refacciones', b'Espera de refacciones'), (b'Terminada', b'Terminada'), (b'Cancelada', b'Cancelada'), (b'Especial', b'Especial')])),
                ('servicio', models.CharField(default=b'Icon', max_length=30, choices=[(b'Icon', b'Icon'), (b'Tecnoservicio', b'Tecnoservicio')])),
                ('zona', models.CharField(default=b'Local', max_length=30, choices=[(b'Local', b'Local'), (b'Foraneo', b'Foraneo')])),
                ('concepto', models.CharField(default=b'Armado', max_length=50, choices=[(b'Armado', b'Armado'), (b'Revision', b'Revision'), (b'OrdenesIcon', b'OrdenesIcon'), (b'Mantenimiento', b'Mantenimiento'), (b'Servicio', b'Servicio')])),
                ('fecha_programada', models.DateField()),
                ('fecha_compra', models.DateField(null=True, blank=True)),
                ('fecha_entrega', models.DateField(null=True, blank=True)),
                ('cliente', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50, blank=True)),
                ('telefono_casa', models.CharField(max_length=20, blank=True)),
                ('telefono_oficina', models.CharField(max_length=20, blank=True)),
                ('telefono_movil', models.CharField(max_length=20, blank=True)),
                ('direccion', models.CharField(max_length=100, blank=True)),
                ('colonia', models.CharField(max_length=50, blank=True)),
                ('municipio_delegacion', models.CharField(max_length=50, blank=True)),
                ('codigo_postal', models.CharField(max_length=5, blank=True)),
                ('entre', models.CharField(max_length=50, blank=True)),
                ('y_entre', models.CharField(max_length=50, blank=True)),
                ('reporta', models.CharField(max_length=100)),
                ('no_serie', models.CharField(max_length=100, blank=True)),
                ('observaciones', models.TextField(blank=True)),
                ('comentarios', models.TextField(blank=True)),
                ('icon_os', models.CharField(max_length=35, blank=True)),
                ('icon_ics', models.CharField(max_length=35, blank=True)),
                ('icon_on', models.CharField(max_length=35, blank=True)),
                ('icon_cn', models.CharField(max_length=35, blank=True)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='ordenes.Marca', null=True)),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='ordenes.Modelo', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=200)),
                ('estado', models.CharField(max_length=100, null=True, blank=True)),
                ('domicilio', models.CharField(max_length=200, null=True, blank=True)),
                ('telefono', models.CharField(max_length=150, null=True, blank=True)),
                ('empresa', models.ForeignKey(blank=True, to='ordenes.Empresa', null=True)),
            ],
        ),
    ]
