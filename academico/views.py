# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User

def main_page(request):
  plantilla = get_template('main_page.html')
  variables = Context({
    'titulo_ventana': '::SIA::',
    'titulo_pagina': 'Bienvenido al SIA',
    'cuerpo': 'Instituto Syspro'
  })
  salida = plantilla.render(variables)
  return HttpResponse(salida)


# def estudiante_pagina(request, username):
  # try:
    # estudiante = User.objects.get(username=username)
  # except:
    # raise Http404('Requested user not found.')
  # bookmarks = estudiante.bookmark_set.all()
  # plantilla = get_template('estudiante_pagina.html')
  # variables = Context({
    # 'username': username,
    # 'bookmarks': bookmarks
  # })
  # r = template.render(plantilla)
  # return HttpResponse(r)