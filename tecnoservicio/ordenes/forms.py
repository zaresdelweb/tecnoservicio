# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from models import *
from tecnoservicio.users.models import User
from django.forms import Textarea
from django.utils.safestring import mark_safe

class HorizRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = (
            'servicio',
            'zona',
            'fecha_programada',
            'concepto',
            'tecnico',
            'cliente',
            'email',
            'telefono_casa',
            'telefono_oficina',
            'telefono_movil',
            'direccion',
            'colonia',
            'municipio_delegacion',
            'codigo_postal',
            'entre',
            'y_entre',
            'reporta',
            'tienda',
            'marca',
            'modelo',
            'no_serie',
            'fecha_compra',
            'fecha_entrega',
            'observaciones',
            'comentarios',
            'icon_os',
            'icon_ics',
            'icon_on',
            'icon_cn',
        )

        widgets={
            'servicio':forms.RadioSelect(renderer=HorizRadioRenderer),
            'zona':forms.RadioSelect(renderer=HorizRadioRenderer),
            'fecha_programada':forms.TextInput(attrs={'class':'form-control','data-date-format':'dd/mm/yyyy','readonly':'readonly','required':'required'}),
            'concepto':forms.RadioSelect(renderer=HorizRadioRenderer),
            'tecnico':forms.Select(attrs={'class':'chosen-select','required':'required'}),
            'cliente':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            'email':forms.TextInput(attrs={'class':'form-control',}),
            'telefono_casa':forms.TextInput(attrs={'class':'form-control',}),
            'telefono_oficina':forms.TextInput(attrs={'class':'form-control',}),
            'telefono_movil':forms.TextInput(attrs={'class':'form-control',}),
            'direccion':forms.TextInput(attrs={'class':'form-control',}),
            'colonia':forms.TextInput(attrs={'class':'form-control',}),
            'municipio_delegacion':forms.TextInput(attrs={'class':'form-control',}),
            'codigo_postal':forms.TextInput(attrs={'class':'form-control',}),
            'entre':forms.TextInput(attrs={'class':'form-control',}),
            'y_entre':forms.TextInput(attrs={'class':'form-control',}),
            'reporta':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            'tienda':forms.Select(attrs={'class':'chosen-select','required':'required'}),
            'marca':forms.Select(attrs={'class':'chosen-select','required':'required'}),
            'modelo':forms.Select(attrs={'class':'chosen-select','required':'required'}),
            'no_serie':forms.TextInput(attrs={'class':'form-control',}),
            'fecha_compra':forms.TextInput(attrs={'class':'form-control date-picker2','data-date-format':'dd/mm/yyyy','readonly':'readonly'}),
            'fecha_entrega':forms.TextInput(attrs={'class':'form-control date-picker2','data-date-format':'dd/mm/yyyy','readonly':'readonly'}),
            'observaciones':forms.Textarea(attrs={'placeholder':'Ingresa las observaciones','rows':'5', 'class':'form-control'}),
            'comentarios':forms.Textarea(attrs={'placeholder':'Ingresa las comentarios','rows':'5', 'class':'form-control'}),
            'icon_os':forms.TextInput(attrs={'class':'form-control',}),
            'icon_ics':forms.TextInput(attrs={'class':'form-control',}),
            'icon_on':forms.TextInput(attrs={'class':'form-control',}),
            'icon_cn':forms.TextInput(attrs={'class':'form-control',}),
        } 

class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = ('nombre','cantidad')
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control',}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control',})
            } 

class Orden_estatusForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ('estatus',)
        widgets={'estatus':forms.Select(attrs={'class':'chosen-select','required':'required'}),} 

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ('mensaje',)
        widgets={'mensaje':forms.Textarea(attrs={'placeholder':'Escribir comentario','rows':'1', 'class':'form-control message-input'}),}

class PublicidadForm(forms.ModelForm):
    class Meta:
        model = Publicidad
        fields = ('ordenes',)