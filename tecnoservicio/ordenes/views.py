# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from django.contrib.auth import login, authenticate, logout
from django.http import Http404
from datetime import datetime
from .forms import *
from .models import *
import json
from tecnoservicio.users.models import *
from django.db.models import Q
import reversion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from tecnoservicio.tareas.tasks import *

def comprobar_orden(request, orden):
	if request.user.perfil == 'Tecnico local' or request.user.perfil == 'Tecnico foraneo':
		if not orden.tecnico == request.user:
			raise Http404
	elif request.user.perfil == 'Vendedor':
		if not orden.servicio == 'Icon':
			raise Http404
	elif request.user.perfil == 'Tienda':
		if not orden.tienda.empresa.usuario == request.user:
			raise Http404
	return True

def filtrar_orden(request, ordenes_list):
	if request.user.perfil == 'Tecnico local' or request.user.perfil == 'Tecnico foraneo':
		ordenes_list = ordenes_list.filter(tecnico = request.user)
	elif request.user.perfil == 'Vendedor':
		ordenes_list = ordenes_list.filter(servicio = 'Icon')
	elif request.user.perfil == 'Tienda':
		ordenes_list = ordenes_list.filter( tienda__empresa__usuario = request.user )
	return ordenes_list

def lista_orden(request):
	if request.method == 'POST':
		busqueda = request.POST.get("buscar", "")
		if not busqueda == '':
			ordenes_list = Orden.objects.filter(Q(folio__contains=busqueda) | Q(cliente__icontains=busqueda)| Q(telefono_casa__contains=busqueda) | Q(telefono_oficina__contains=busqueda) | Q(telefono_movil__contains=busqueda) | Q(tecnico__username__icontains=busqueda)  | Q(icon_os__contains=busqueda) | Q(icon_ics__contains=busqueda) | Q(icon_on__contains=busqueda) | Q(icon_cn__contains=busqueda) | Q(no_serie__contains=busqueda)).order_by('-id')
		else:
			ordenes_list = []
	else:
		ordenes_list = Orden.objects.all()
	ordenes_list = filtrar_orden(request, ordenes_list)
	paginator = Paginator(ordenes_list, 35)
	page = request.GET.get('page')
	try:
		ordenes = paginator.page(page)
	except PageNotAnInteger:
		ordenes = paginator.page(1)
	except EmptyPage:
		ordenes = paginator.page(paginator.num_pages)
	return render(request, 'ordenes/orden_lista.html', locals())

def alta_orden(request):
	form = OrdenForm()
	conceptoform = ConceptoForm()
	tecnicos_locales = serializers.serialize("json", User.objects.filter(perfil = 'Tecnico local', is_active = True), fields=('username',))
	tecnicos_foraneos = serializers.serialize("json", User.objects.filter(perfil = 'Tecnico foraneo', is_active = True), fields=('username',))
	if request.method == "POST":
		form = OrdenForm(request.POST)
		if form.is_valid():
			o = form.save(commit = False)
			o.operador = request.user
			o.estatus = 'Nueva'
			o.save()
			conceptoform = ConceptoForm(request.POST)
			if conceptoform.is_valid():
				nombre = conceptoform.cleaned_data.get("nombre", "")
				cantidad = conceptoform.cleaned_data.get("cantidad", "")
				if nombre and cantidad:
					concepto = conceptoform.save(commit = False)
					concepto.orden = o
					concepto.usuario = request.user
					corte = Corte()
					concepto.corte = corte.asignar()
					concepto.save()
			return HttpResponseRedirect(reverse( 'editar_orden', args=[o.folio]))
		else:
			messages.warning(request, 'Algo salió mal, intenta de nuevo.')
	return render(request, 'ordenes/orden_form.html', locals())

def editar_orden(request, folio):
	orden = Orden.objects.filter(folio = folio)[0]
	comprobar_orden(request, orden)
	mensajes_orden = Mensaje.objects.filter(orden = orden)
	form = OrdenForm(instance = orden)
	conceptoform = ConceptoForm()
	mensaje = MensajeForm()
	orden_estatus = Orden_estatusForm(instance = orden)
	tecnicos_locales = serializers.serialize("json", User.objects.filter(perfil = 'Tecnico local', is_active = True), fields=('username',))
	tecnicos_foraneos = serializers.serialize("json", User.objects.filter(perfil = 'Tecnico foraneo', is_active = True), fields=('username',))
	if request.method == "POST":
		if 'guardar' in request.POST:
			form = OrdenForm(request.POST, instance = orden)
			orden_estatus = Orden_estatusForm(request.POST, instance = orden)
			if form.is_valid() and orden_estatus.is_valid():
				o = form.save()
				orden_estatus.save()
				conceptoform = ConceptoForm(request.POST)
				if conceptoform.is_valid():
					nombre = conceptoform.cleaned_data.get("nombre", "")
					cantidad = conceptoform.cleaned_data.get("cantidad", "")
					if nombre and cantidad:
						concepto = conceptoform.save(commit = False)
						concepto.orden = o
						concepto.usuario = request.user
						corte = Corte()
						concepto.corte = corte.asignar()
						concepto.save()
			else:
				messages.warning(request, 'Algo salió mal, intenta de nuevo.')
		if 'enviar_comentarios' in request.POST:
			mensaje = MensajeForm(request.POST)
			if mensaje.is_valid():
				o = mensaje.save(commit=False)
				o.usuario = request.user
				o.orden = orden
				o.save()
				conceptoform = ConceptoForm(request.POST)
	conceptos = Concepto.objects.filter(orden = orden)
	version_list = reversion.get_for_object(orden)
	mensaje = MensajeForm()
	if request.user.perfil == 'Tecnico local' or request.user.perfil == 'Tecnico foraneo':
		return render(request, 'ordenes/orden_info.html', locals())
	return render(request, 'ordenes/orden_form.html', locals())

def imprimir_orden(request, folio):
	orden = Orden.objects.filter(folio=folio)[0]
	comprobar_orden(request, orden)
	hoy = datetime.datetime.now()
	publicidad = Publicidad.objects.all()
	return render(request, 'ordenes/imprimir_orden.html', locals())

def calendario(request,tipo):
	if tipo == 'locales':
		tipo='Local'
	elif tipo == 'foraneas':
		tipo='Foraneo'
	fecha = datetime.datetime.now()
	ordenes = Orden.objects.filter(fecha_programada__year = fecha.year, fecha_programada__month = fecha.month, zona=tipo)
	ordenes = filtrar_orden(request, ordenes)
	return render(request, 'ordenes/calendario.html', locals())

def publicidad(request):
	form = PublicidadForm()
	if request.method == 'POST':
		form = PublicidadForm(request.POST, request.FILES)
		if form.is_valid():
			Publicidad.objects.all().delete()
			form.save()
	publicidad = Publicidad.objects.all()
	return render(request, 'ordenes/publicidad_form.html', locals())

def lista_cortes(request):
	objects = Corte.objects.all()
	return render(request, 'ordenes/corte_lista.html', locals())

def generar_corte(request, id):
	corte = Corte.objects.filter(id = id)[0]
	corte.cortado = True
	corte.save()
	return HttpResponseRedirect(reverse('lista_cortes'))

def corte(request, id):
	ordenes = []
	corte = Corte.objects.filter(id = id)[0]
	conceptos = Concepto.objects.filter(corte=corte)
	total = 0
	for concepto in conceptos:
		total += concepto.cantidad
		if not concepto.orden in ordenes:
			ordenes.append(concepto.orden)
	return render(request, 'ordenes/corte.html', locals())

def reportes(request):
	hoy = datetime.datetime.now()
	return render(request, 'ordenes/reportes.html', locals())

def ordenes_icon(request,inicio,fin):
	inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
	fin = datetime.datetime.strptime(fin, '%d-%m-%Y')
	objects = Orden.objects.filter(fecha_alta__range=(inicio, fin), servicio='Icon', concepto='Armado')
	return render(request, 'ordenes/reporte_ordenes.html', locals())

def ordenes_tecno(request,inicio,fin):
	inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
	fin = datetime.datetime.strptime(fin, '%d-%m-%Y')
	objects = Orden.objects.filter(fecha_alta__range=(inicio, fin), servicio='Tecnoservicio', concepto='Armado')
	return render(request, 'ordenes/reporte_ordenes.html', locals())

def armados_locales(request,inicio,fin):
	inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
	fin = datetime.datetime.strptime(fin, '%d-%m-%Y')
	objects = Orden.objects.filter(fecha_alta__range=(inicio, fin), servicio='Icon', concepto='Armado', zona='Local')
	return render(request, 'ordenes/reporte_ordenes.html', locals())

def armados_foraneos(request,inicio,fin):
	inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
	fin = datetime.datetime.strptime(fin, '%d-%m-%Y')
	objects = Orden.objects.filter(fecha_alta__range=(inicio, fin), servicio='Icon', concepto='Armado', zona='Foraneo')
	return render(request, 'ordenes/reporte_ordenes.html', locals())

@csrf_exempt
def actualizar_marca(request):
	if request.method == 'POST':
		tienda = request.POST.get('tienda')
		marca = serializers.serialize("json", Marca.objects.filter(tienda__id = tienda), fields=('nombre',))
		return HttpResponse(marca,content_type="application/json")
	else:
		return HttpResponse(json.dumps({"actualizar_marca": "ok"}),content_type="application/json")
		
@csrf_exempt
def actualizar_modelo(request):
	if request.method == 'POST':
		marca = request.POST.get('marca')
		modelo = serializers.serialize("json", Modelo.objects.filter(marca__id = marca), fields=('nombre',))
		return HttpResponse(modelo,content_type="application/json")
	else:
		return HttpResponse(json.dumps({"actualizar_modelo": "ok"}),content_type="application/json")

@csrf_exempt
def calendario_ordenes(request):
	from lib import JsonPropertySerializer
	if request.method == 'POST':
		fecha = request.POST.get('fecha').split('/')
		tipo = request.POST.get('tipo')
		fecha = datetime.datetime(year=int(fecha[2]), month=int(fecha[1]), day=int(fecha[0]))
		ordenes = JsonPropertySerializer().serialize(Orden.objects.filter(fecha_programada__year = fecha.year, fecha_programada__month = fecha.month, zona=tipo))
		return HttpResponse(ordenes,content_type="application/json")
	else:
		return HttpResponse(json.dumps({"calendario_ordenes": "ok"}),content_type="application/json")

