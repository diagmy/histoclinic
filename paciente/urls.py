from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import logout
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^api/paciente/motivoconsultas/agregar/$', views.MotivoConsultaAgregar.as_view()),
    url(r'^api/paciente/motivoconsultas/(?P<pk>\d+)/$', views.MotivoConsultaDetalle.as_view()),
    url(r'^api/paciente/motivoconsultas/(?P<pk>\d+)/editar/$', views.MotivoConsultaEditar.as_view()),
    url(r'^api/paciente/motivoconsultas/(?P<pk>\d+)/borrar/$', views.MotivoConsultaBorrar.as_view()),
    url(r'^api/paciente/motivoconsultas/$', views.MotivoConsulta.as_view()),
    # url(r'^login/$', views.create_user1,{},name='login'),
    # url(r'^accounts/login/$', views.create_user1,{},name='login'),
    url(r'^accounts/signin$', views.SigninView.as_view(),name='login'),
    url(r'^add/user/$', views.add_user,{},name='add_user'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),

    url(r'^api/paciente/agregar/$', views.PacienteAgregar.as_view()),
    url(r'^api/pacientes/$', views.PacienteLista.as_view()),
    url(r'^api/paciente/(?P<pk>\d+)/$', views.PacienteDetalle.as_view()),
    url(r'^api/paciente/edit/$', views.PacienteEditarr.as_view()),
    url(r'^api/paciente/(?P<pk>\d+)/editar/$', views.PacienteEditar.as_view()),
    url(r'^api/paciente/(?P<pk>\d+)/borrar/$', views.PacienteBorrar.as_view()),



    url(r'^api/paciente/alergia/agregar/$', views.AlergiaAgregar1.as_view()),
url(r'^api/paciente/alergia/agregar1/$', views.AlergiaAgregar2.as_view()),
    url(r'^api/paciente/alergias/$', views.Alergia.as_view()),
    url(r'^api/paciente/alergias/(?P<pk>\d+)/$', views.AlergiaDetalle.as_view()),

    url(r'^api/paciente/alergias/(?P<pk>\d+)/editar/$', views.AlergiaEditar.as_view()),
    url(r'^api/paciente/alergias/(?P<pk>\d+)/borrar/$', views.AlergiaBorrar.as_view()),
    url(r'^api/paciente/alergias/edit/$', views.AlergiaEdit.as_view()),
    url(r'^api/paciente/alergias/get/(?P<pk>\d+)/$', views.AlergiaGet.as_view()),

    url(r'^api/paciente/seguro/agregar/$', views.SeguroAgregar.as_view()),
    url(r'^api/paciente/seguro/(?P<pk>\d+)/$', views.SeguroDetalle.as_view()),
    url(r'^api/paciente/seguro/get/(?P<pk>\d+)/$', views.SeguroGet.as_view()),
    url(r'^api/paciente/seguro/edit/$', views.SeguroEdit.as_view()),
    url(r'^api/paciente/seguro/(?P<pk>\d+)/editar/$', views.SeguroEditar.as_view()),
    url(r'^api/paciente/seguro/(?P<pk>\d+)/borrar/$', views.SeguroBorrar.as_view()),
    url(r'^api/paciente/seguro/$', views.Seguro.as_view()),

url(r'^api/paciente/vacunas/$', views.Inmunizacion.as_view()),
    url(r'^api/paciente/vacunas/agregar/$', views.InmunizacionAgregar.as_view()),
    url(r'^api/paciente/vacunas/(?P<pk>\d+)/$', views.InmunizacionDetalle.as_view()),
    url(r'^api/paciente/vacunas/edit/$', views.InmunizacionEdit.as_view()),
    url(r'^api/paciente/vacunas/(?P<pk>\d+)/borrar/$', views.InmunizacionBorrar.as_view()),
    url(r'^api/paciente/vacunas-get/(?P<pk>\d+)/$', views.InmunizacionGet.as_view()),
    url(r'^api/paciente/vacunas/(?P<pk>\d+)/editar/$', views.InmunizacionEditar.as_view()),


    url(r'^api/paciente/antecendentes-personales-patologicos/agregar/$', views.AntecendentePersonalPatologicoAgregar.as_view()),
    url(r'^api/paciente/antecendentes-personales-patologicos/(?P<pk>\d+)/$', views.AntecendentePersonalPatologicoDetalle.as_view()),
    url(r'^api/paciente/antecendentes-personales-get/(?P<pk>\d+)/$', views.AntecendentePersonalPatologicoget.as_view()),
    url(r'^api/paciente/antecendentes-personales-patologicos/edit/$', views.AntecendentePersonalPatologicoEdit.as_view()),
    url(r'^api/paciente/antecendentes-personales-patologicos/(?P<pk>\d+)/borrar/$', views.AntecendentePersonalPatologicoBorrar.as_view()),
    url(r'^api/paciente/antecendentes-personales-patologicos/(?P<pk>\d+)/editar/$', views.AntecendentePersonalPatologicoEditar.as_view()),
    url(r'^api/paciente/antecendentes-personales-patologicos/$', views.AntecendentePersonalPatologicoDetalle.as_view()),

    url(r'^api/paciente/antecendentes-familiares-patologicos/agregar/$', views.AntecendenteFamiliarPatologicoAgregar.as_view()),
    url(r'^api/paciente/antecendentes-familiares-get/(?P<pk>\d+)/$', views.AntecendenteFamiliarPatologicoget.as_view()),
    url(r'^api/paciente/antecendentes-familiares-patologicos/edit/$', views.AntecendenteFamiliarPatologicoEdit.as_view()),
    url(r'^api/paciente/antecendentes-familiares-patologicos/(?P<pk>\d+)/$', views.AntecendenteFamiliarPatologicoDetalle.as_view()),
    url(r'^api/paciente/antecendentes-familiares-patologicos/(?P<pk>\d+)/borrar$', views.AntecendenteFamiliarPatologicoBorrar.as_view()),
    url(r'^api/paciente/antecendentes-familiares-patologicos/(?P<pk>\d+)/editar$', views.AntecendenteFamiliarPatologicoEditar.as_view()),
    url(r'^api/paciente/antecendentes-familiares-patologicos/$', views.AntecendenteFamiliarPatologicoDetalle.as_view()),

    url(r'^api/paciente/padecimiento-actual/agregar/$', views.PadecimientoActualAgregar.as_view()),
    url(r'^api/paciente/padecimiento-actual/(?P<pk>\d+)/editar/$', views.PadecimientoActualEditar.as_view()),
    url(r'^api/paciente/padecimiento-actual/(?P<pk>\d+)/borrar/$', views.PadecimientoActualBorrar.as_view()),
    url(r'^api/paciente/padecimiento-actual/$', views.PadecimientoActual.as_view()),
    url(r'^api/paciente/padecimiento-actual/(?P<pk>\d+)/$', views.PadecimientoActualDetalle.as_view()),
    url(r'^api/paciente/padecimiento-actual/get/(?P<pk>\d+)/$', views.PadecimientoActualGet.as_view()),
    url(r'^api/paciente/padecimiento-actual/edit/$', views.PadecimientoActualEdit.as_view()),



    url(r'^api/paciente/medicamentos/(?P<pk>\d+)/$', views.Medicamento.as_view()),
    url(r'^api/paciente/medicamentos/edit/$', views.MedicamentoEdit.as_view()),
    url(r'^api/paciente/medicamentos/get/(?P<pk>\d+)/$', views.MedicamentoGet.as_view()),
    url(r'^api/paciente/medicamentos/agregar/$', views.MedicamentoAgregar.as_view()),


    url(r'^api/paciente/signos_vitales/(?P<pk>\d+)/$', views.SignoVital.as_view()),
    url(r'^api/paciente/signos-vitales/agregar/edit/$', views.SignoVitalAgregarEdit.as_view()),
    url(r'^api/paciente/signos_vitales_get/(?P<id>\d+)/$', views.SignoVital_get.as_view()),
    url(r'^api/paciente/signos-vitales/agregar/$', views.SignoVitalAgregar.as_view()),



    url(r'^api/paciente/Otras_Ordenes_get/(?P<id>\d+)/$', views.OtraOrdenTerapeuticaGet.as_view()),
    url(r'^api/paciente/otras-ordenes/(?P<pk>\d+)/$', views.OtraOrdenTerapeutica.as_view()),
    url(r'^api/paciente/otras-ordenes/agregar/$', views.OtraOrdenTerapeuticaoAgregar.as_view()),
    url(r'^api/paciente/otras-ordenes/agregar/edit/$', views.OtraOrdenTerapeuticaoAgregarEdit.as_view()),

    url(r'^api/paciente/evolucion/(?P<pk>\d+)/$', views.Evolucion.as_view()),
    url(r'^api/paciente/evolucion/get/(?P<pk>\d+)/$', views.EvolucionGet.as_view()),
    url(r'^api/paciente/evolucion/agregar/edit/$', views.EvolucionEdit.as_view()),

    url(r'^api/paciente/evolucion/agregar/$', views.EvolucionAgregar.as_view()),


    url(r'^api/paciente/revision-sistema/(?P<pk>\d+)/$', views.RevisionPorSistema.as_view()),
    url(r'^api/paciente/revision-sistema/get/(?P<pk>\d+)/$', views.RevisionPorSistemaGet.as_view()),
    url(r'^api/paciente/revision-sistema/edit/$', views.RevisionPorSistemaEdit.as_view()),
    url(r'^api/paciente/revision-sistema/agregar/$', views.RevisionPorSistemaAgregar.as_view()),

]