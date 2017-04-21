from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.landing_page, name='landing_page'),
url(r'^profile/page/help/$', views.page_profile_info, name='profile_help'),
url(r'^signup/$', views.signup, name='signup1'),
url(r'^accounts/login/$', views.login1,name='login'),
url(r'^paciente/$', views.patients, name='paciente'),
url(r'^formulario-paciente/$', views.form_wizard, name='formulario-paciente'),



]
