# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0009_auto_20150513_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordenes', models.ImageField(help_text=b'Este es el archivo que se muestra en las ordenes', upload_to=b'publicidad', verbose_name=b'Publicidad de las ordenes')),
            ],
        ),
    ]
