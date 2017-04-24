from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, requires_csrf_token
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext
from paciente.models import Paciente
from paciente.models import UserProfile
from django.views.decorators.http import require_POST, require_GET



def landing_page(request):
	print ("\n\n\n\n\n\n\n") 
	print (request)
	print ("\n\n\n\n\n\n\n")
	return render(request,'inicio.html',{})


def page_profile_info(request):
  return render(request,'perfil-paciente.html')


def signup(request):
 return render(request,'signupform.html')


def patients(request):
 return render(request,'pacientes-lista.html')

def form_wizard(request):
 return render(request,'formulario-paciente.html')


def login1(request):
 return render(request,'page_user_login_1.html')

@requires_csrf_token
def form_perfil(request):
	if request.method == 'POST':
		data = request.POST; image = request.FILES['prof_img']
		nombre = data['nombre']; apellifo = data['apellifo']; telefono = data['telefono']; celular = data['celular']
		fs = FileSystemStorage()
		filename = fs.save("username.jpg", image)
		#import your models here from obj = Paciente.objects.create(user=......) and so on then obj.save()
	return render(request, 'perfil-usuario.html')

@csrf_exempt
def ajax_form(request):
	if request.method == "POST":
		file = request.FILES.get('fileToUpload')
		print (file)
		return HttpResponse()