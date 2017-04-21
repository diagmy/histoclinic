from rest_framework import serializers
from .models import Paciente, MotivoConsultas, PadecimientoActuales, Alergias, Signos_Vitales, Medicamentos, Otras_Ordenes_Terapeuticas, Evoluciones, Seguros, AntecendentesPersonalesPatologicos, Inmunizaciones, AntecedentesFamiliaresPatologicos, RevisionesporSistema

class PacienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paciente
        fields = '__all__'

class MotivoConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MotivoConsultas
        fields = '__all__'

class PadecimientoActualSerializer(serializers.ModelSerializer):

    class Meta:
        model = PadecimientoActuales
        fields = '__all__'

class AlergiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alergias
        fields = '__all__'

class SignoVitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signos_Vitales
        fields = '__all__'

class MedicamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicamentos
        fields = '__all__'

class OtraOrdenTerapeuticaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Otras_Ordenes_Terapeuticas
        fields = '__all__'

class EvolucionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evoluciones
        fields = '__all__'

class SeguroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seguros
        fields = '__all__'

class AntecendentePersonalPatologicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AntecendentesPersonalesPatologicos
        fields = '__all__'

class InmunizacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inmunizaciones
        fields = '__all__'

class AntecendenteFamiliarPatologicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AntecedentesFamiliaresPatologicos
        fields = '__all__'

class RevisionPorSistemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = RevisionesporSistema
        fields = '__all__'

