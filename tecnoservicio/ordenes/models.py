# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.timezone import now
from .choices import *
import uuid
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
import datetime
from tecnoservicio.users.models import *
from reversion import register, create_revision, set_ignore_duplicates
import reversion
from config.settings.common import DOMINIO, DEFAULT_FROM_EMAIL
from django.core.urlresolvers import reverse
import pytz
utc=pytz.UTC

class Orden(models.Model):

	folio = models.PositiveIntegerField(unique=True)
	fecha_alta = models.DateTimeField(auto_now_add=True, editable=True)
	operador = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True)
	tecnico = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, null=True)
	estatus = models.CharField(max_length=30, choices=Estatus)
	servicio = models.CharField(max_length=30, choices=Servicio, default="Icon")
	zona = models.CharField(max_length=30, choices=Zonas, default="Local")
	concepto = models.CharField(max_length=50, choices=Concepto, default="Armado")
	fecha_programada = models.DateField()
	fecha_compra = models.DateField(blank=True, null=True)
	fecha_entrega = models.DateField(blank=True, null=True)
	cliente = models.CharField(max_length=100)
	email = models.CharField(max_length=50, blank=True)
	telefono_casa = models.CharField(max_length=20, blank=True)
	telefono_oficina = models.CharField(max_length=20, blank=True)
	telefono_movil = models.CharField(max_length=20, blank=True)
	direccion = models.CharField(max_length=100, blank=True)
	colonia = models.CharField(max_length=50, blank=True)
	municipio_delegacion = models.CharField(max_length=50, blank=True)
	codigo_postal = models.CharField(max_length=5, blank=True)
	entre = models.CharField(max_length=50, blank=True)
	y_entre = models.CharField(max_length=50, blank=True)
	reporta = models.CharField(max_length=100)
	tienda = models.ForeignKey('Tienda', on_delete=models.SET_NULL, null=True)
	marca = models.ForeignKey('Marca', on_delete=models.SET_NULL, null=True)
	modelo = models.ForeignKey('Modelo', on_delete=models.SET_NULL, null=True)
	no_serie = models.CharField(max_length=100, blank=True)
	observaciones = models.TextField(blank=True,)
	comentarios = models.TextField(blank=True,)
	icon_os = models.CharField(max_length=35, blank=True)
	icon_ics = models.CharField(max_length=35, blank=True)
	icon_on = models.CharField(max_length=35, blank=True)
	icon_cn = models.CharField(max_length=35, blank=True)

	class Meta:
		ordering = ['-folio']

	def save(self, *args, **kwargs):
		with create_revision():
			set_ignore_duplicates(True)
			concepto = False
			primer_tecnico = False
			if not self.pk:
				try:
					self.folio = Orden.objects.all().order_by('-folio')[0].folio + 1
				except:
					self.folio = 10100
				if self.servicio == 'Icon' and self.concepto == 'Armado':
					concepto = Concepto()
					concepto.nombre = 'Orden de armado'
					concepto.cantidad = 333.5
					concepto.usuario = self.operador
				if self.servicio == 'Icon' and self.concepto == 'Revision':
					concepto = Concepto()
					concepto.nombre = 'Icon revision'
					concepto.cantidad = 609
					concepto.usuario = self.operador
				if self.servicio == 'Icon' and self.concepto == 'OrdenesIcon':
					concepto = Concepto()
					concepto.nombre = 'Orden Icon'
					concepto.cantidad = 609
					concepto.usuario = self.operador
				if self.servicio == 'Icon' and self.concepto == 'Mantenimiento':
					concepto = Concepto()
					concepto.nombre = 'Icon mantenimiento'
					concepto.cantidad = 609
					concepto.usuario = self.operador
				if self.servicio == 'Icon' and self.concepto == 'Servicio':
					concepto = Concepto()
					concepto.nombre = 'Icon servicio'
					concepto.cantidad = 609
					concepto.usuario = self.operador

				primer_tecnico = Tecnico_orden()
				primer_tecnico.tecnico = self.tecnico
				primer_tecnico.usuario = self.operador
				

			else:
				orig = Orden.objects.get(id=self.id)
				if orig.tecnico != self.tecnico:
					tecnico_orden = Tecnico_orden()
					tecnico_orden.tecnico = self.tecnico
					tecnico_orden.usuario = self.operador
					tecnico_orden.orden = self
					tecnico_orden.save(concepto_nombre='**Cambio de tecnico ('+orig.tecnico.username+' a '+self.tecnico.username+')')

			super(Orden, self).save(*args, **kwargs)

			if concepto:
				concepto.orden = self
				corte = Corte()
				concepto.corte = corte.asignar()
				concepto.save()

			if primer_tecnico:
				primer_tecnico.orden = self
				primer_tecnico.save(concepto_nombre='**Nuevo tecnico (' + self.tecnico.username +')')

	def _color(self):
		if self.estatus == 'Nueva':
			return  '#898989'
		elif self.estatus == 'Alerta':
			return '#EA4459'
		elif self.estatus == 'Espera de refacciones':
			return '#F69F45'
		elif self.estatus == 'Terminada':
			return '#136DBC'
		elif self.estatus == 'Cancelada':
			return '#434343'
		elif self.estatus == 'Especial':
			return '#262626'

	color = property(_color)

	def modificaciones(self):
		try:
			version_list = reversion.get_for_object(self)
			numero_veces = len(version_list)
			ultimo_usuario = version_list[0].revision.user
			ultima_fecha = version_list[0].revision.date_created
			cambio_tecnico = Tecnico_orden.objects.filter(orden = self)
			return numero_veces, ultimo_usuario, ultima_fecha, cambio_tecnico
		except:
			return '','','',''


	def actualizar(self):

		if self.fecha_alta < utc.localize(datetime.datetime.now() - datetime.timedelta(days=3)):
			self.estatus = 'Alerta'
			self.save()
			fail_silently = True
			c = Context({
				'tecnico': self.tecnico.username,
				'folio': str(self.folio),
				'link': reverse( 'editar_orden', args=[self.id]),
				'dominio': DOMINIO,
				})
			html_content = get_template('email/mail_alerta_orden.html').render(c)
			plaintext = get_template('email/mail_alerta_orden.txt').render(c)
			msg = EmailMultiAlternatives(
				subject="Notificación de usuario",
				body=plaintext,
				from_email=DEFAULT_FROM_EMAIL,
				to= ('rampzodia1@gmail.com',),
			)
			msg.attach_alternative(html_content, "text/html")
			msg.send(fail_silently)
			print 'Mail enviado'
		else:
			print 'No enviado'

	def total(self):
		total = 0
		conceptos = Concepto.objects.filter(orden = self).exclude(nombre__contains='**')
		for concepto in conceptos:
			total += concepto.cantidad
		return total

reversion.register(Orden)

class Concepto(models.Model):
	nombre = models.CharField('Concepto', max_length=100, blank=True, null=True)
	cantidad = models.FloatField(max_length=35, blank=True, null=True)
	orden = models.ForeignKey(Orden, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	corte = models.ForeignKey('Corte', related_name='+')
	fecha = models.DateTimeField(auto_now_add=True)

class Tecnico_orden(models.Model):
	tecnico = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	fecha = models.DateTimeField(auto_now_add=True)
	orden = models.ForeignKey(Orden)
	def save(self, concepto_nombre=None, *args, **kwargs):
		concepto = Concepto()
		if concepto_nombre:
			concepto.nombre = concepto_nombre
		else:
			concepto.nombre = 'Cambio de técnico'
		concepto.cantidad = -200
		concepto.orden = self.orden
		concepto.usuario = self.usuario
		corte = Corte()
		concepto.corte = corte.asignar()
		concepto.save()
		super(Tecnico_orden, self).save(*args, **kwargs)

class Corte(models.Model):
	creado = models.DateTimeField(auto_now_add=True)
	fecha_corte = models.DateTimeField(null=True, blank=True)
	cortado = models.BooleanField(default=False)
	def __unicode__(self):
		return str(self.id)
	def asignar(self):
		try:
			o = Corte.objects.filter(cortado = False)[0]
			return o
		except:
			corte = Corte()
			corte.save()
			return corte

	class Meta:
		ordering = ['-id']

class Empresa(models.Model):
	nombre = models.CharField(max_length=200, unique=True)
	usuario = models.ForeignKey(User)
	def __unicode__(self):
		return self.nombre

class Tienda(models.Model):
	empresa = models.ForeignKey('Empresa', null=True, blank=True)
	nombre = models.CharField(max_length=200, unique=True)
	estado = models.CharField(max_length=100, null=True, blank=True)
	domicilio = models.CharField(max_length=200, null=True, blank=True)
	telefono = models.CharField(max_length=150, null=True, blank=True)
	def __unicode__(self):
		return self.nombre

class Marca(models.Model):
	tienda = models.ManyToManyField('Tienda')
	nombre = models.CharField(max_length=100, unique=True,)
	def __unicode__(self):
		return self.nombre

class Modelo(models.Model):
	marca = models.ForeignKey('Marca')
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=200, blank=True)
	def __unicode__(self):
		return self.nombre

class Mensaje(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	orden = models.ForeignKey('Orden')
	fecha_hora = models.DateTimeField(auto_now_add=True)
	mensaje = models.TextField()
	def __unicode__(self):
		return self.mensaje
	class Meta:
		ordering = ['fecha_hora']

class Publicidad(models.Model):
	ordenes = models.ImageField(upload_to='publicidad', verbose_name='Publicidad de las ordenes', help_text='Este es el archivo que se muestra en las ordenes')