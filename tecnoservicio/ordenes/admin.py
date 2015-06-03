# -*- encoding: utf-8 -*-
from models import *
from forms import *
from django.contrib import admin
import reversion



class OrdenAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Orden, OrdenAdmin)
admin.site.register(Empresa)
admin.site.register(Tienda)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Mensaje)
admin.site.register(Concepto)
admin.site.register(Corte)
admin.site.register(Publicidad)