# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0005_auto_20150513_1628'),
    ]

    operations = [
        migrations.RenameField(
            model_name='concepto',
            old_name='concepto',
            new_name='nombre',
        ),
    ]
