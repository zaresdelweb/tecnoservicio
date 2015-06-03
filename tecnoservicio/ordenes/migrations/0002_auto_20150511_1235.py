# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ordenes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='operador',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='tecnico',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='tienda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='ordenes.Tienda', null=True),
        ),
        migrations.AddField(
            model_name='modelo',
            name='marca',
            field=models.ForeignKey(to='ordenes.Marca'),
        ),
        migrations.AddField(
            model_name='marca',
            name='tienda',
            field=models.ManyToManyField(to='ordenes.Tienda'),
        ),
    ]
