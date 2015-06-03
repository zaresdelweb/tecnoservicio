# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0010_publicidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='colores',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
