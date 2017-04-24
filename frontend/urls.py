from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.landing_page, name='landing_page'),
	url(r'^perfil-paciente/$', views.page_profile_info, name='profile_help'),
	url(r'^crear-cuenta/$', views.signup, name='signup1'),
	url(r'^cuenta/iniciar-sesion/$', views.login1,name='login'),
	url(r'^paciente/$', views.patients, name='paciente'),
	url(r'^formulario-paciente/$', views.form_wizard, name='formulario-paciente'),
	url(r'^perfil-usuario/$', views.form_perfil, name='perfil-usuario'),
	url(r'^perfil-usuario/upload$', views.ajax_form, name='perfil-usuario-upload'),



]
