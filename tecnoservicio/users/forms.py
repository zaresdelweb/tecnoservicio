# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from .models import User


class UserForm(forms.ModelForm):

	class Meta:
		# Set this form to use the User model.
		model = User
		# Constrain the UserForm to just these fields.
		fields = ("first_name", "last_name")

class UsuarioForm(forms.ModelForm):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="Introduce el password")
	email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput, required=False)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Los passwords no coinciden")
		return password2
	
	class Meta:
		# Set this form to use the User model.
		model = User
		# Constrain the UserForm to just these fields.
		fields = ("username", "email", "password1", "password2", "perfil")

class Usuario_editarForm(forms.ModelForm):
	email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput, required=False)

	class Meta:
		# Set this form to use the User model.
		model = User
		# Constrain the UserForm to just these fields.
		fields = ("username", "email", "perfil")

class PasswordForm(forms.ModelForm):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="Introduce el password")

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Los passwords no coinciden")
		return password2
	
	class Meta:
		# Set this form to use the User model.
		model = User
		# Constrain the UserForm to just these fields.
		fields = ("password1", "password2")


