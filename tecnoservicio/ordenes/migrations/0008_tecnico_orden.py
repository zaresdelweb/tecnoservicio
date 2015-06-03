# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ordenes', '0007_auto_20150513_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tecnico_orden',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('orden', models.ForeignKey(to='ordenes.Orden')),
                ('tecnico', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('usuario', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
