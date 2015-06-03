# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ordenes', '0002_auto_20150511_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('mensaje', models.TextField()),
                ('orden', models.ForeignKey(to='ordenes.Orden')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['fecha_hora'],
            },
        ),
    ]
