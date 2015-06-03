# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0006_auto_20150513_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='concepto',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 13, 22, 27, 7, 782530, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='concepto',
            name='nombre',
            field=models.CharField(max_length=35, null=True, verbose_name=b'Concepto', blank=True),
        ),
    ]
