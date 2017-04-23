from django.core.mail import message
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.contrib import messages
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from rest_framework import status
from .models import Paciente, MotivoConsultas, PadecimientoActuales, Alergias, Signos_Vitales, Medicamentos, \
    Otras_Ordenes_Terapeuticas, Evoluciones, AntecendentesPersonalesPatologicos, Seguros, \
    AntecendentesPersonalesPatologicos, Inmunizaciones, AntecedentesFamiliaresPatologicos, RevisionesporSistema
from .serializers import PacienteSerializer, MotivoConsultaSerializer, PadecimientoActualSerializer, AlergiaSerializer, \
    SignoVitalSerializer, MedicamentoSerializer, OtraOrdenTerapeuticaSerializer, EvolucionSerializer, \
    InmunizacionSerializer, SeguroSerializer, AntecendentePersonalPatologicoSerializer, \
    AntecendenteFamiliarPatologicoSerializer, RevisionPorSistemaSerializer, UserSerializer
from rest_framework import generics
import json
from django.views.generic.edit import FormView, BaseDetailView,View

from django.shortcuts import render
from .forms import *

from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.
# list all patients or create new one
# paciente
# -
@ensure_csrf_cookie
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.info(request, "This user already exist.")
            return redirect('add_user')
        elif User.objects.filter(email=request.POST.get('email')).exists():
            messages.info(request, "This Email already exist.")
            return redirect('add_user')
        else:
            user1 = User.objects.create(username=request.POST.get('username'),
                                        password=make_password(request.POST.get('password')),
                                        first_name=request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name'),
                                        email=request.POST.get('email'))
            user1.save()
            user2 = UserProfile.objects.create(user=user1,
                                               state=request.POST.get('state'))
            user2.save()
            messages.info(request, "Your Account is Successfully Created.")
            return redirect(reverse('add_user'))


    else:
        user_form = SignupForm()
        profile_form = SignupFormExtend()
    return render(request, 'signupform.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
class SigninView(APIView):


    def post(self, request):
        data = request.data
        if not data['username'] or not data['password']:
            return Response({'errors': {'__all__': ['Email and Password are required']}},
                            status=status.HTTP_200_OK)

        check_user = User.objects.filter(username__iexact=data['username'])
        if check_user.exists():
            user = check_user.first()
            password = data['password']

            if user is not None and user.check_password(password):
                payload = jwt_payload_handler(user)
                access_token = jwt_encode_handler(payload)
                user1 = UserProfile.objects.get(user_id=user.id)


                return Response({'result': 'success','access_token':access_token,'username':user.username,
                                 'state':user1.state,'is_superuser':user.is_superuser},
                                status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'__all__': ['Email and Password are not matched']}},
                                status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'__all__': ['Email and Password are not matched']}},
                            status=status.HTTP_200_OK)


def create_user1(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:

            login(request, user)
            return redirect('landing_page')
        else:
            messages.info(request,'Your username or password is incorrect.')
            return redirect('login')
    else:
        user_form = SignupForm()

    return render(request, 'page_user_login_1.html', {
        'user_form': user_form,

    })

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        request.session.clear()
        logout(request)
        return HttpResponse('success')


class Search(APIView):

    def get(self, request):
        data = request.GET.get('q')
        # data = '%' + data + '%'
        splitted = data.split(' ')
        l = len(splitted)

        # by_firstname = User.objects.filter(firstname__contains=data)
        by_fullname = []
        by_firstname = []
        by_lastname = []
        by_username = []

        by_firstname = User.objects.filter(first_name__contains=splitted[0])
        if l > 1:
            by_fullname = by_firstname.filter(last_name__contains=splitted[1])
            by_lastname = User.objects.filter(last_name__contains=splitted[1])
        else:
            by_lastname = User.objects.filter(last_name__contains=splitted[0])

        by_username = User.objects.filter(username__contains=splitted[0])
        exact_user = by_username.filter(username=data)

        # print("firstname", by_firstname)
        # print ("lastname", by_lastname)
        # print ("fullname", by_fullname)
        # print ("username", by_username)
        # print ("exact user", exact_user)

        all = []
        if l > 1:
            all = exact_user | by_fullname | by_firstname | by_username | by_lastname
        else:
            all = exact_user | by_firstname | by_username | by_lastname

        serializer = UserSerializer(all, many=True)

        print (serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PacienteLista(APIView):
    def get(self, request):
        pacientes = Paciente.objects.all()
        serializer = PacienteSerializer(pacientes, many=True)
        return Response(serializer.data)


class PacienteDetalle(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PacienteSerializer

    def get_queryset(self):
        return Paciente.objects.filter(id=self.kwargs['pk'])


class PacienteAgregar(generics.CreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class PacienteEditar(generics.UpdateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class PacienteEditarr(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PacienteEditarr, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = Paciente.objects.get(id=get_data['id'])
        if get_data['title'] == 'profile':
            get_obj.apellido = get_data['lname']
            get_obj.nombre = get_data['fname']
            get_obj.edad = get_data['job']
            get_obj.save()
        else:
            get_obj.telefono = get_data['Telefono']
            get_obj.celular = get_data['celular']
            get_obj.tutor = get_data['Tutor']
            get_obj.direccion = get_data['direction']
            get_obj.peso = get_data['peso']
            get_obj.sexo = get_data['sexo']
            get_obj.save()
        return HttpResponse('success')


class PacienteBorrar(generics.DestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


########

class MotivoConsulta(APIView):
    def get(self, request):
        motivoConsultas = MotivoConsultas.objects.all()
        serializer = MotivoConsultaSerializer(motivoConsultas, many=True)
        return Response(serializer.data)


class MotivoConsultaAgregar(generics.CreateAPIView):
    serializer_class = MotivoConsultaSerializer

    def get_queryset(self):
        return MotivoConsultas.objects.filter(paciente=self.kwargs['pk'])


class MotivoConsultaEditar(generics.UpdateAPIView):
    serializer_class = MotivoConsultaSerializer

    def get_queryset(self):
        return MotivoConsultas.objects.filter(paciente=self.kwargs['pk'])


class MotivoConsultaBorrar(generics.DestroyAPIView):
    serializer_class = MotivoConsultaSerializer

    def get_queryset(self):
        return MotivoConsultas.objects.filter(paciente=self.kwargs['pk'])


class MotivoConsultaDetalle(generics.RetrieveAPIView):
    serializer_class = MotivoConsultaSerializer

    def get_queryset(self):
        return MotivoConsultas.objects.filter(paciente=self.kwargs['pk'])


##############

class PadecimientoActual(generics.ListAPIView):
    serializer_class = PadecimientoActualSerializer

    def get_queryset(self):
        return PadecimientoActuales.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass


class PadecimientoActualAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PadecimientoActualAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = PadecimientoActuales.objects.create(padecimiento=get_data['cabeza'],
                                                      paciente=pat,

                                                      )
        get_obj.save()
        return HttpResponse('success')


class PadecimientoActualEditar(generics.UpdateAPIView):
    serializer_class = PadecimientoActualSerializer

    def get_queryset(self):
        return PadecimientoActuales.objects.filter(paciente=self.kwargs['pk'])


class PadecimientoActualBorrar(generics.DestroyAPIView):
    serializer_class = PadecimientoActualSerializer

    def get_queryset(self):
        return PadecimientoActuales.objects.filter(paciente=self.kwargs['pk'])


class PadecimientoActualDetalle(generics.ListAPIView):
    serializer_class = PadecimientoActualSerializer

    def get_queryset(self):
        return PadecimientoActuales.objects.filter(paciente=self.kwargs['pk'])

class PadecimientoActualGet(generics.ListAPIView):
    serializer_class = PadecimientoActualSerializer

    def get_queryset(self):
        return PadecimientoActuales.objects.filter(id=self.kwargs['pk'])


class PadecimientoActualEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PadecimientoActualEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST

        get_obj = PadecimientoActuales.objects.get(id=get_data['id'])
        get_obj.padecimiento = get_data['padecimiento']

        get_obj.save()
        return HttpResponse('success')

#######

class Alergia(generics.ListAPIView):
    serializer_class = AlergiaSerializer

    def get_queryset(self):
        return Alergias.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass

class AlergiaAgregar1(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AlergiaAgregar1, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = Alergias.objects.create(tipo=get_data['tipo'],
                                          nombre_alergia=get_data['alergia'],
                                          activo = get_data['activo'],
                                          paciente=pat,

                                          )
        get_obj.save()
        return HttpResponse('success')




class AlergiaEditar(generics.UpdateAPIView):
    serializer_class = AlergiaSerializer

    def get_queryset(self):
        return Alergias.objects.filter(paciente=self.kwargs['pk'])


class AlergiaBorrar(generics.DestroyAPIView):
    serializer_class = AlergiaSerializer

    def get_queryset(self):
        return Alergias.objects.filter(paciente=self.kwargs['pk'])


class AlergiaDetalle(generics.ListAPIView):
    serializer_class = AlergiaSerializer

    def get_queryset(self):
        return Alergias.objects.filter(paciente_id=self.kwargs['pk'])


class AlergiaGet(generics.ListAPIView):
    serializer_class = AlergiaSerializer

    def get_queryset(self):
        return Alergias.objects.filter(id=self.kwargs['pk'])


class AlergiaEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AlergiaEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = Alergias.objects.get(id=get_data['id'])
        get_obj.tipo = get_data['Tipo']
        get_obj.nombre_alergia = get_data['Nombre']
        get_obj.activo = get_data['Activo']
        get_obj.save()
        return HttpResponse('success')

###########

class Seguro(generics.ListAPIView):
    serializer_class = SeguroSerializer

    def get_queryset(self):
        return Seguros.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass


class SeguroAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SeguroAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = Seguros.objects.create(nombre_seguro=get_data['nombre_seguro'],
                                         numero_afiliado=get_data['numero_afiliado'],
                                         paciente=pat,
                                         )
        get_obj.save()
        return HttpResponse('success')


class SeguroEditar(generics.UpdateAPIView):
    serializer_class = SeguroSerializer

    def get_queryset(self):
        return Seguros.objects.filter(paciente=self.kwargs['pk'])


class SeguroBorrar(generics.DestroyAPIView):
    serializer_class = SeguroSerializer

    def get_queryset(self):
        return Seguros.objects.filter(paciente=self.kwargs['pk'])


class SeguroGet(generics.ListAPIView):
    serializer_class = SeguroSerializer

    def get_queryset(self):
        return Seguros.objects.filter(id=self.kwargs['pk'])


class SeguroEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SeguroEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = Seguros.objects.get(id=get_data['id'])
        get_obj.nombre_seguro = get_data['Nom']
        get_obj.numero_afiliado = get_data['Ase']
        get_obj.save()
        return HttpResponse('success')


class SeguroDetalle(generics.ListAPIView):
    serializer_class = SeguroSerializer

    def get_queryset(self):
        return Seguros.objects.filter(paciente=self.kwargs['pk'])


########

class Inmunizacion(generics.ListAPIView):
    serializer_class = InmunizacionSerializer

    def get_queryset(self):
        return Inmunizaciones.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass


class InmunizacionEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InmunizacionEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = Inmunizaciones.objects.get(id=get_data['id'])
        get_obj.nombre_vacuna = get_data['Vac']
        get_obj.dosis_aplicadas = get_data['Dos']
        get_obj.edad_aplicacion = get_data['Edad']
        get_obj.save()
        return HttpResponse('success')


class InmunizacionAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InmunizacionAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = Inmunizaciones.objects.create(tarjeta_vacunacion=get_data['tarjeta_vacunacion'],
                                                edad_aplicacion=get_data['edad_aplicacion'],
                                                dosis_aplicadas=get_data['dosis_aplicadas'],
                                                nombre_vacuna=get_data['nombre_vacuna'],
                                                paciente=pat,
                                                )
        get_obj.save()
        return HttpResponse('success')

class InmunizacionGet(generics.ListAPIView):
    serializer_class = InmunizacionSerializer

    def get_queryset(self):
        return Inmunizaciones.objects.filter(id=self.kwargs['pk'])


class InmunizacionEditar(generics.UpdateAPIView):
    serializer_class = InmunizacionSerializer

    def get_queryset(self):
        return Inmunizaciones.objects.filter(paciente=self.kwargs['pk'])


class InmunizacionBorrar(generics.DestroyAPIView):
    serializer_class = InmunizacionSerializer

    def get_queryset(self):
        return Inmunizaciones.objects.filter(paciente=self.kwargs['pk'])


class InmunizacionDetalle(generics.ListAPIView):
    serializer_class = InmunizacionSerializer

    def get_queryset(self):
        return Inmunizaciones.objects.filter(paciente=self.kwargs['pk'])

########

class AntecendentePersonalPatologico(generics.ListAPIView):
    serializer_class = AntecendentePersonalPatologicoSerializer

    def get_queryset(self):
        return Evoluciones.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass


class AntecendentePersonalPatologicoAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AntecendentePersonalPatologicoAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = AntecendentesPersonalesPatologicos.objects.create(antepersopatologico=get_data['antepersopatologico'],
                                                                    paciente=pat,
                                                                    )
        get_obj.save()
        return HttpResponse('success')


class AntecendentePersonalPatologicoEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AntecendentePersonalPatologicoEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = AntecendentesPersonalesPatologicos.objects.get(id=get_data['id'])
        get_obj.fecha = get_data['date']
        get_obj.antepersopatologico = get_data['detail']
        get_obj.save()
        return HttpResponse('success')


class AntecendentePersonalPatologicoget(generics.ListAPIView):
    serializer_class = AntecendentePersonalPatologicoSerializer

    def get_queryset(self):
        return AntecendentesPersonalesPatologicos.objects.filter(id=self.kwargs['pk'])


class AntecendentePersonalPatologicoBorrar(generics.DestroyAPIView):
    serializer_class = AntecendentePersonalPatologicoSerializer

    def get_queryset(self):
        return Evoluciones.objects.filter(paciente=self.kwargs['pk'])


class AntecendentePersonalPatologicoDetalle(generics.ListAPIView):
    serializer_class = AntecendentePersonalPatologicoSerializer

    def get_queryset(self):
        return AntecendentesPersonalesPatologicos.objects.filter(paciente=self.kwargs['pk'])


class AntecendentePersonalPatologicoEditar(generics.UpdateAPIView):
    serializer_class = AntecendentePersonalPatologicoSerializer

    def get_queryset(self):
        return Evoluciones.objects.filter(paciente=self.kwargs['pk'])


#####

class AntecendenteFamiliarPatologicoget(generics.ListAPIView):
    serializer_class = AntecendenteFamiliarPatologicoSerializer

    def get_queryset(self):
        return AntecedentesFamiliaresPatologicos.objects.filter(id=self.kwargs['pk'])


class AntecendenteFamiliarPatologicoEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AntecendenteFamiliarPatologicoEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = AntecedentesFamiliaresPatologicos.objects.get(id=get_data['id'])
        get_obj.enfermedad = get_data['En']
        get_obj.parentesco = get_data['Pa']
        get_obj.antefamipatologicos = get_data['Notas']
        get_obj.save()
        return HttpResponse('success')


class AntecendenteFamiliarPatologico(generics.ListAPIView):
    serializer_class = AntecendenteFamiliarPatologicoSerializer

    def get_queryset(self):
        return AntecedentesFamiliaresPatologicos.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass


class AntecendenteFamiliarPatologicoAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AntecendenteFamiliarPatologicoAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = AntecedentesFamiliaresPatologicos.objects.create(enfermedad=get_data['enfermedad'],
                                                                   parentesco=get_data['parentesco'],
                                                                   antefamipatologicos=get_data['antefamipatologicos'],
                                                                   paciente=pat,

                                                                   )
        get_obj.save()
        return HttpResponse('success')


class AntecendenteFamiliarPatologicoDetalle(generics.ListAPIView):
    serializer_class = AntecendenteFamiliarPatologicoSerializer

    def get_queryset(self):
        return AntecedentesFamiliaresPatologicos.objects.filter(paciente=self.kwargs['pk'])


class AntecendenteFamiliarPatologicoBorrar(generics.DestroyAPIView):
    serializer_class = AntecendenteFamiliarPatologicoSerializer

    def get_queryset(self):
        return AntecedentesFamiliaresPatologicos.objects.filter(paciente=self.kwargs['pk'])


class AntecendenteFamiliarPatologicoEditar(generics.UpdateAPIView):
    serializer_class = AntecendenteFamiliarPatologicoSerializer

    def get_queryset(self):
        return AntecedentesFamiliaresPatologicos.objects.filter(paciente=self.kwargs['pk'])


######
class SignoVital(generics.ListAPIView):
    serializer_class = SignoVitalSerializer

    def get_queryset(self):
        return Signos_Vitales.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass

class SignoVital_get(generics.ListAPIView):
    serializer_class = SignoVitalSerializer

    def get_queryset(self):
        return Signos_Vitales.objects.filter(id=self.kwargs['id'])

class SignoVitalAgregarEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignoVitalAgregarEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST

        get_obj = Signos_Vitales.objects.get(id=get_data['id'])
        get_obj.tension_arterial = get_data['Tension_Arterial']
        get_obj.frecuencia_cardiaca = get_data['Frecuencia_Cardiaca']
        get_obj.frecuencia_respiratoria = get_data['Frecuencia_Respiratoria']
        get_obj.temperatura = get_data['Temperatura']
        get_obj.notas = get_data['Notas']
        get_obj.save()

        return HttpResponse('success')


class SignoVitalAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignoVitalAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = Signos_Vitales.objects.create(tension_arterial=get_data['Tension_Arterial'],
                                                frecuencia_cardiaca=get_data['Frecuencia_Cardiaca'],
                                                frecuencia_respiratoria=get_data['Frecuencia_Respiratoria'],
                                                temperatura= get_data['Temperatura'],
                                                notas= get_data['Notas'],
                                                paciente =pat ,

                                                )
        get_obj.save()
        return HttpResponse('success')

#########

class Medicamento(generics.ListAPIView):
    serializer_class = MedicamentoSerializer

    def get_queryset(self):
        return Medicamentos.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass


class MedicamentoGet(generics.ListAPIView):
    serializer_class = MedicamentoSerializer

    def get_queryset(self):
        return Medicamentos.objects.filter(id=self.kwargs['pk'])


class MedicamentoEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MedicamentoEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = Medicamentos.objects.get(id=get_data['id'])
        get_obj.fecha = get_data['Fec']
        get_obj.nombre = get_data['Nom']
        get_obj.dosis = get_data['Dos']
        get_obj.frecuencia = get_data['Fre']
        get_obj.via = get_data['Via']
        get_obj.save()
        return HttpResponse('success')

class MedicamentoAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MedicamentoAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = Medicamentos.objects.create(nombre=get_data['Nombre'],
                                              dosis=get_data['Dosis'],
                                              frecuencia=get_data['Frecuencia'],
                                              via=get_data['Via'],
                                              nota=get_data['Nota'],
                                              paciente=pat,

                                              )
        get_obj.save()
        return HttpResponse('success')

###########
class OtraOrdenTerapeutica(generics.ListAPIView):
    serializer_class = OtraOrdenTerapeuticaSerializer

    def get_queryset(self):
        return Otras_Ordenes_Terapeuticas.objects.filter(paciente=self.kwargs['pk'])



class OtraOrdenTerapeuticaoAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OtraOrdenTerapeuticaoAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = Otras_Ordenes_Terapeuticas.objects.create(dieta=get_data['dieta'],
                                                            actividad_fisica=get_data['actividad_fisica'],
                                                            activo=get_data['activo'],
                                                            oxigeno=get_data['Oxigeno'],
                                                            curas=get_data['curas'],
                                                            fisioterapia_respiratoria=get_data['fisioterapia_respiratoria'],
                                                            sondas_drenajes=get_data['sondas_drenajes'],
                                                            estudios_lab_diagnostico=get_data['estudios_lab_diagnostico'],
                                                            paciente=pat,
                                                            )
        get_obj.save()
        return HttpResponse('success')

class OtraOrdenTerapeuticaoAgregarEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OtraOrdenTerapeuticaoAgregarEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = Otras_Ordenes_Terapeuticas.objects.get(id=get_data['id'])
        get_obj.dieta = get_data['dieta1']
        get_obj.activo = get_data['activo21']
        get_obj.actividad_fisica = get_data['actividadfisica1']
        get_obj.curas = get_data['curas1']
        get_obj.fisioterapia_respiratoria = get_data['fisioterapiarespiratoria1']
        get_obj.sondas_drenajes = get_data['sondas1']
        get_obj.estudios_lab_diagnostico = get_data['estudioslabdiagnostico1']
        get_obj.save()
        return HttpResponse('success')

class OtraOrdenTerapeuticaGet(generics.ListAPIView):
    serializer_class = OtraOrdenTerapeuticaSerializer

    def get_queryset(self):
        return Otras_Ordenes_Terapeuticas.objects.filter(id=self.kwargs['id'])
#######
class Evolucion(generics.ListAPIView):
    serializer_class = EvolucionSerializer

    def get_queryset(self):
        return Evoluciones.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass

class EvolucionEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EvolucionEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = Evoluciones.objects.get(id=get_data['id'])
        get_obj.notas = get_data['notas']
        get_obj.save()
        return HttpResponse('success')


class EvolucionGet(generics.ListAPIView):
    serializer_class = EvolucionSerializer

    def get_queryset(self):
        return Evoluciones.objects.filter(id=self.kwargs['pk'])



class EvolucionAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EvolucionAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = Evoluciones.objects.create(notas=get_data['notas'],
                                             paciente=pat,
                                             )
        get_obj.save()
        return HttpResponse('success')




######
class RevisionPorSistema(generics.ListAPIView):
    serializer_class = RevisionPorSistemaSerializer

    def get_queryset(self):
        return RevisionesporSistema.objects.filter(paciente=self.kwargs['pk'])

    def post(self):
        pass

class RevisionPorSistemaEdit(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RevisionPorSistemaEdit, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        get_obj = RevisionesporSistema.objects.get(id=get_data['id'])
        get_obj.cabeza = get_data['cabeza']
        get_obj.save()
        return HttpResponse('success')

class RevisionPorSistemaGet(generics.ListAPIView):
    serializer_class = RevisionPorSistemaSerializer

    def get_queryset(self):
        return RevisionesporSistema.objects.filter(id=self.kwargs['pk'])

class RevisionPorSistemaAgregar(FormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RevisionPorSistemaAgregar, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_data = request.POST
        pat = Paciente.objects.get(id=get_data['id'])
        get_obj = RevisionesporSistema.objects.create(cabeza=get_data['cabeza'],
                                                      paciente=pat,
                                                      )
        get_obj.save()
        return HttpResponse('success')