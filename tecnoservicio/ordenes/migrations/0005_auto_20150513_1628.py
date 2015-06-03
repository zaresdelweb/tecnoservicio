# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ordenes', '0004_auto_20150513_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='concepto',
            name='usuario',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='concepto',
            name='corte',
            field=models.ForeignKey(related_name='+', to='ordenes.Corte'),
        ),
    ]
