# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ordenes', '0012_remove_orden_colores'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corte',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='orden',
            options={'ordering': ['-folio']},
        ),
        migrations.AddField(
            model_name='empresa',
            name='usuario',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
