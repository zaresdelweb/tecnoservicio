# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.db import models
from .choices import *
from config.settings.common import DOMINIO, DEFAULT_FROM_EMAIL


from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils.translation import ugettext_lazy as _

from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

class User(AbstractUser):

	perfil  = models.CharField(max_length=25, choices=Perfiles, default="Operador")

	def __unicode__(self):
		return self.username

	def mail_usuario(self, password):

		fail_silently = True

		c = Context({
			'usuario': self,
			'password': password, 
			'dominio': DOMINIO, 
			})

		html_content = get_template('email/mail_usuario_alta.html').render(c)
		plaintext = get_template('email/mail_usuario_alta.txt').render(c)

		msg = EmailMultiAlternatives(
			subject="Notificación de usuario",
			body=plaintext,
			from_email=DEFAULT_FROM_EMAIL,
			to= (self.email,),
		)

		msg.attach_alternative(html_content, "text/html")

		msg.send(fail_silently)
			
