# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0011_orden_colores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orden',
            name='colores',
        ),
    ]
