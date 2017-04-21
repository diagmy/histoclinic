from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
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