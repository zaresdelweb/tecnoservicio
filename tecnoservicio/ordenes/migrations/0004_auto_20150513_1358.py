# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0003_mensaje'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concepto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('concepto', models.CharField(max_length=35, null=True, blank=True)),
                ('cantidad', models.FloatField(max_length=35, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Corte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('fecha_corte', models.DateTimeField(null=True, blank=True)),
                ('cortado', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='concepto',
            name='corte',
            field=models.ForeignKey(to='ordenes.Corte'),
        ),
        migrations.AddField(
            model_name='concepto',
            name='orden',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ordenes.Orden', null=True),
        ),
    ]
