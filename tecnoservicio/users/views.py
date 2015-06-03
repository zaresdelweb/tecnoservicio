# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from braces.views import LoginRequiredMixin

from .forms import *
from .models import User

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth import logout


def inicio(request):
    return render(request, 'pages/inicio.html', locals())

def salir(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def mi_password(request):
    form = PasswordForm()
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password1")
            request.user.set_password(password)
            request.user.save()
            messages.info(request, 'Cambiamos tu contraseña')
            return HttpResponseRedirect(reverse('inicio'))
    return render(request, 'users/password_form.html', locals())

def lista_usuario(request):
    objects = User.objects.all()
    return render(request, 'users/usuario_lista.html', locals())

def alta_usuario(request):
    form = UsuarioForm()
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password1")
            o = form.save(commit=False)
            o.set_password(password)
            o.save()
            messages.info(request, 'Se dió de alta el usuario: '+ o.username.encode('utf-8'))
            return HttpResponseRedirect(reverse('lista_usuario'))
    return render(request, 'users/usuario_form.html', locals())

def editar_usuario(request, id):
    usuario = User.objects.filter(id = id)[0]
    form = Usuario_editarForm(instance= usuario)
    if request.method == "POST":
        form = Usuario_editarForm(request.POST, instance=usuario)
        if form.is_valid():
            o = form.save()
            messages.info(request, 'Se modificó exitosamente el usuario: '+ o.username.encode('utf-8'))
            return HttpResponseRedirect(reverse('lista_usuario'))
    return render(request, 'users/usuario_form.html', locals())

def eliminar_usuario(request, id):
    user = User.objects.filter(id=id)[0]
    nombre = user.username
    user.delete()
    messages.info(request, 'Se eliminó con exito el usuario: ' + nombre)
    return HttpResponseRedirect(reverse('lista_usuario'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
