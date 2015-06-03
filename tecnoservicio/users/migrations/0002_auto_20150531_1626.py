# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='perfil',
            field=models.CharField(default='Operador', max_length=25, choices=[(b'Administrador', b'Administrador'), (b'Tecnico local', b'Tecnico local'), (b'Tecnico foraneo', b'Tecnico foraneo'), (b'Operador', b'Operador'), (b'Tienda', b'Tienda'), (b'Vendedor', b'Vendedor')]),
        ),
    ]
