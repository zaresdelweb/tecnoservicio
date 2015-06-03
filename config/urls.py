# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^inicio/$', 'tecnoservicio.users.views.inicio', name='inicio'),
    url(r'^salir/$', 'tecnoservicio.users.views.salir', name='salir'),
    url(r'^mi-password/$', 'tecnoservicio.users.views.mi_password', name='mi_password'),

    url(r'^lista-usuarios/$', 'tecnoservicio.users.views.lista_usuario', name='lista_usuario'),
    url(r'^alta-usuarios/$', 'tecnoservicio.users.views.alta_usuario', name='alta_usuario'),
    url(r'^editar-usuario/(.+)/$', 'tecnoservicio.users.views.editar_usuario', name='editar_usuario'),
    url(r'^eliminar-usuario/(.+)/$', 'tecnoservicio.users.views.eliminar_usuario', name='eliminar_usuario'),

    url(r'^lista-ordenes/$', 'tecnoservicio.ordenes.views.lista_orden', name='lista_orden'),
    url(r'^alta-orden/$', 'tecnoservicio.ordenes.views.alta_orden', name='alta_orden'),
    url(r'^editar-orden/(.+)/$', 'tecnoservicio.ordenes.views.editar_orden', name='editar_orden'),
    url(r'^imprimir-orden/(.+)/$', 'tecnoservicio.ordenes.views.imprimir_orden', name='imprimir_orden'),

    url(r'^calendario/(.+)/$', 'tecnoservicio.ordenes.views.calendario', name='calendario'),

    url(r'^publicidad/$', 'tecnoservicio.ordenes.views.publicidad', name='publicidad'),

    url(r'^lista-cortes/$', 'tecnoservicio.ordenes.views.lista_cortes', name='lista_cortes'),
    url(r'^generar-corte/(.+)/$', 'tecnoservicio.ordenes.views.generar_corte', name='generar_corte'),
    url(r'^corte/(.+)/$', 'tecnoservicio.ordenes.views.corte', name='corte'),

    url(r'^reportes/$', 'tecnoservicio.ordenes.views.reportes', name='reportes'),
    url(r'^ordenes-icon/(.+)/(.+)/$', 'tecnoservicio.ordenes.views.ordenes_icon', name='ordenes_icon'),
    url(r'^ordenes-tecno/(.+)/(.+)/$', 'tecnoservicio.ordenes.views.ordenes_tecno', name='ordenes_tecno'),
    url(r'^armados-locales/(.+)/(.+)/$', 'tecnoservicio.ordenes.views.armados_locales', name='armados_locales'),
    url(r'^armados-foraneos/(.+)/(.+)/$', 'tecnoservicio.ordenes.views.armados_foraneos', name='armados_foraneos'),

    url(r'^manual/usuario/$', TemplateView.as_view(template_name='ordenes/manual_usuarios.html'), name="manual_usuarios"),
    url(r'^manual/iconfield/$', TemplateView.as_view(template_name='ordenes/manual_iconfield.html'), name="manual_iconfield"),

    # AJAX
    url(r'^actualizar_marca/$', 'tecnoservicio.ordenes.views.actualizar_marca', name='actualizar_marca'),
    url(r'^actualizar_modelo/$', 'tecnoservicio.ordenes.views.actualizar_modelo', name='actualizar_modelo'),
    url(r'^calendario_ordenes/$', 'tecnoservicio.ordenes.views.calendario_ordenes', name='calendario_ordenes'),

    # Django Admin (Comment the next line to disable the admin)
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("tecnoservicio.users.urls", namespace="users")),
    url(r'^acceso/', include('allauth.urls')),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
