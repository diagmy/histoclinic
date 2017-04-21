import binascii
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Paciente(models.Model):

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField(blank= True, null = True)
    seleccion_sexo= (('M', 'Masculino'), ('F', 'Femenino'))
    sexo = models.CharField(max_length=100, choices=seleccion_sexo, blank=True)
    peso = models.FloatField(max_length=5, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=100, blank=True)
    celular = models.CharField(max_length=100, blank=True)
    fecha_ingreso = models.DateField(auto_now_add=True, blank=False)
    hora_ingreso = models.DateTimeField(auto_now_add=True, blank=False)
    tutor = models.CharField(max_length=100, blank=True)
    cedula_tutor = models.CharField(max_length=100, blank=True)
    cedula_paciente = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return self.nombre

    def get_url(self):
         return '/paciente/{0}/{0}'.format(self.id)


class UserProfile(models.Model):
    select_group  = (
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('infero', 'Infero'),

    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    state = models.CharField(max_length=255, choices=select_group, default='doctor')

class MotivoConsultas(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.DateTimeField(auto_now_add=True)
    motivo_consulta = models.CharField(max_length=150, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

class PadecimientoActuales(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    padecimiento = models.CharField(max_length=100, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)


class Alergias(models.Model):
    seleccion_tipoAler= (('Medicamento', 'Medicamento'), ('Alimentos', 'Alimentos'), ('Ambiente', 'Ambiente'), ('Otros', 'Otros'))    
    tipo = models.CharField(max_length=12, choices=seleccion_tipoAler, blank =True)
    nombre_alergia = models.CharField(max_length=20, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    seleccion_alergia_activa =(('Si', 'Si'), ('No', 'No'))
    activo = models.CharField(max_length=2, choices=seleccion_alergia_activa, blank=True)
    fecha = models.DateField(auto_now_add=True, blank=True, null =True)

class Signos_Vitales(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    tension_arterial = models.CharField(max_length=20, blank=True)
    frecuencia_cardiaca = models.CharField(max_length=20, blank=True)
    frecuencia_respiratoria = models.CharField(max_length=20, blank=True)
    temperatura = models.CharField(max_length=20, blank=True)
    notas = models.CharField(max_length=100, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)



class Medicamentos(models.Model):
    nombre = models.CharField(max_length=30, blank=True)
    tipo = models.CharField(max_length=20, blank=True)
    dosis = models.CharField(max_length=40, blank=True)
    frecuencia = models.CharField(max_length=30, blank=True)
    via = models.CharField(max_length=20, blank=True)
    nota = models.CharField(max_length=40, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    seleccion_medicamento_activo =(('Si', 'Si'), ('No', 'No'))
    activo = models.CharField(max_length=2, choices=seleccion_medicamento_activo, blank=True)
    fecha = models.DateField(auto_now_add=True, blank=True, null =True)
    
class Otras_Ordenes_Terapeuticas(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    dieta = models.CharField(max_length=60, blank=True)
    actividad_fisica = models.CharField(max_length=30, blank=True)
    curas = models.CharField(max_length=30, blank=True)
    oxigeno = models.CharField(max_length=20, blank=True)
    fisioterapia_respiratoria = models.CharField(max_length=20, blank=True)
    sondas_drenajes = models.CharField(max_length=20, blank=True)
    estudios_lab_diagnostico = models.CharField(max_length=60, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    seleccion_ordenes_activa =(('Si', 'Si'), ('No', 'No'))
    activo = models.CharField(max_length=2, choices=seleccion_ordenes_activa, blank=True)

class Evoluciones(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    notas = models.CharField(max_length=200, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

class Seguros(models.Model):
    nombre_seguro = models.CharField(max_length=30, blank=True)
    numero_afiliado = models.CharField(max_length=20, blank=True )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    seleccion_seguro_activo =(('Si', 'Si'), ('No', 'No'))
    activo = models.CharField(max_length=2, choices=seleccion_seguro_activo, blank=True)

class AntecendentesPersonalesPatologicos(models.Model):
    fecha = models.DateField(auto_now_add=True, blank=True)
    hora = models.TimeField(auto_now_add=True, blank=True)
    antepersopatologico = models.CharField(max_length=200, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

class Inmunizaciones(models.Model):
    seleccion_tarjetavacuna =(('Si', 'Si'), ('No', 'No'))
    tarjeta_vacunacion = models.CharField(max_length=2, choices=seleccion_tarjetavacuna, blank=True)
    nombre_vacuna = models.CharField(max_length=20, blank=True, null=True)
    dosis_aplicadas = models.IntegerField(blank=True, null =True)
    edad_aplicacion = models.IntegerField(blank=True, null = True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True, blank=True, null =True)

class AntecedentesFamiliaresPatologicos(models.Model):
    enfermedad = models.CharField(max_length=50, blank=True)
    seleccion_parentesco= (('Padre', 'Padre'), ('Madre', 'Madre'), ('Abuelos', 'Abuelos'), ('Hermanos', 'Hermanos'), ('Otros', 'Otros'))
    parentesco = models.CharField(max_length=9, choices=seleccion_parentesco, blank=True)
    antefamipatologicos = models.CharField(max_length=200,blank=True )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

class RevisionesporSistema(models.Model):
    fecha = models.DateField(auto_now_add=True, blank=True)
    hora = models.TimeField(auto_now_add=True, blank=True)
    cabeza = models.CharField(max_length=200, blank=True)
    ojos = models.CharField(max_length=200, blank=True)
    oidos = models.CharField(max_length=200, blank=True)
    nariz = models.CharField(max_length=200, blank=True)
    boca = models.CharField(max_length=200, blank= True)
    respiratorio = models.CharField(max_length=200, blank =True)
    cardiovascular = models.CharField(max_length=200, blank=True)
    gastrointestinal = models.CharField(max_length=200, blank=True)
    urinario = models.CharField(max_length=200, blank=True)
    neuromuscular = models.CharField(max_length=200, blank=True)
    psiquismo = models.CharField(max_length=200, blank=True)
    conducta = models.CharField(max_length=200, blank=True)
    piel = models.CharField(max_length=200, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

