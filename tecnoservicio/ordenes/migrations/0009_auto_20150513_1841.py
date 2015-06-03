# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0008_tecnico_orden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concepto',
            name='nombre',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Concepto', blank=True),
        ),
    ]
