from django.contrib import admin
from .models import Paciente,UserProfile, MotivoConsultas, PadecimientoActuales, Alergias, Seguros, Signos_Vitales, Medicamentos, Otras_Ordenes_Terapeuticas, Evoluciones, AntecendentesPersonalesPatologicos, Seguros, Inmunizaciones, AntecedentesFamiliaresPatologicos, RevisionesporSistema

# Register your models here.
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nombre","telefono")
admin.site.register(Paciente,PacienteAdmin)

class PacienteMotivoConsultaAdmin(admin.ModelAdmin):
    list_display = ("fecha","motivo_consulta")
admin.site.register(MotivoConsultas,PacienteMotivoConsultaAdmin)

class PadecimientoActualAdmin(admin.ModelAdmin):
    list_display = ("paciente","padecimiento")
admin.site.register(PadecimientoActuales,PadecimientoActualAdmin)

class AlergiasAdmin(admin.ModelAdmin):
    list_display = ("paciente","tipo")
admin.site.register(Alergias,AlergiasAdmin)

class SignosVitalesAdmin(admin.ModelAdmin):
    list_display = ("fecha", "paciente")
admin.site.register(Signos_Vitales, SignosVitalesAdmin)

class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ("paciente", "nombre")
admin.site.register(Medicamentos, MedicamentoAdmin)

class OtrasOrdenesTerapeuticasAdmin(admin.ModelAdmin):
    list_display = ("paciente", "fecha", "hora")
admin.site.register(Otras_Ordenes_Terapeuticas, OtrasOrdenesTerapeuticasAdmin)

class EvolucionAdmin(admin.ModelAdmin):
    list_display = ("fecha", "paciente", "notas")
admin.site.register(Evoluciones, EvolucionAdmin)

class AntecedentesPersonalesPatologicosAdmin(admin.ModelAdmin):
    list_display = ("paciente", "antepersopatologico")
admin.site.register(AntecendentesPersonalesPatologicos, AntecedentesPersonalesPatologicosAdmin)



admin.site.register(UserProfile)
class InmunizacionesAdmin(admin.ModelAdmin):
    list_display = ("paciente", "tarjeta_vacunacion")
admin.site.register(Inmunizaciones, InmunizacionesAdmin)

class AntecedentesFamiliaresPatologicosAdmin(admin.ModelAdmin):
    list_display = ("paciente", "antefamipatologicos", "parentesco")
admin.site.register(AntecedentesFamiliaresPatologicos ,AntecedentesFamiliaresPatologicosAdmin)

class RevisionporSistemaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "paciente")
admin.site.register(RevisionesporSistema, RevisionporSistemaAdmin)

class SegurosAdmin(admin.ModelAdmin):
    list_display = ("nombre_seguro", "paciente")
admin.site.register(Seguros, SegurosAdmin)