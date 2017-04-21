
from django import template
from django.shortcuts import render

from paciente.models import Paciente
from paciente.forms import AntecedentesFamiliaresPatologicosForm
register = template.Library()


@register.filter(name='patient')
def patient(user):
    return Paciente.objects.all()


@register.filter(name='choices1')
def choices1():
    forms = AntecedentesFamiliaresPatologicosForm()
    return forms