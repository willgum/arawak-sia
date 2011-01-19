# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import *                   # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                    # se incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                   
from django.contrib.auth.models import Group
from academico.models import Profesor, Estudiante, TipoDocumento, Genero, Estrato

def indice(request):
    plantilla = "index.html",
    variables = Context({
        'user': request.user, 
        'titulo': '.: SIA - Sistema de Información Académica :.',
        'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
        'path': settings.MEDIA_URL,
    })
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))

def perfil(request):
    plantilla = "perfil.html",
    grupos = request.user.groups.all()    
    if grupos is not None:
        for grupo in grupos:
            grupoUsuario = Group.objects.get(name = grupo)
        if grupoUsuario.id == 3 or grupoUsuario.id == 4:
            if grupoUsuario.id == 3:
                usuario = Profesor.objects.get(documento = request.user)
            else:
                usuario = Estudiante.objects.get(documento = request.user)
            variables = Context({
            'user': request.user, 
            'titulo': '.: SIA - Sistema de Información Académica :.',
            'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
            'path': settings.MEDIA_URL,
            'usuario': usuario,
            'tipoDocumento': TipoDocumento.objects.get(codigo = usuario.tipo_documento_id),
            'genero': Genero.objects.get(codigo = usuario.genero_id),
            'estratos': Estrato.objects
            })            
        else :
            variables = Context({
                'user': request.user, 
                'titulo': '.: SIA - Sistema de Información Académica :.',
                'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
                'path': settings.MEDIA_URL,
                'msg_error': 'Lo sentimos, no se puede tener acceso a su perfil.',
            })
    return render_to_response(plantilla, variables, context_instance=RequestContext(request))

def actulizarperfil(request):
    grupos = request.user.groups.all()    
    if grupos is not None:
        for grupo in grupos:
            grupoUsuario = Group.objects.get(name = grupo)
        if grupoUsuario.id == 3 or grupoUsuario.id == 4:
            if grupoUsuario.id == 3:
                usuario = Profesor.objects.get(documento = request.user)
            else:
                usuario = Estudiante.objects.get(documento = request.user)  
            
            usuario.direccion = request.POST['direccion']
            usuario.lugar_residencia = request.POST['lugar']
            usuario.telefono = request.POST['fijo']
            usuario.movil = request.POST['celular']
            usuario.email = request.POST['email']
            usuario.web = request.POST['web'] 
            usuario.save()  
            request.user.message_set.create(message="Los datos fueron guardados exitosamente.")
    return HttpResponseRedirect("/perfil/")

def login(request):
    username = request.POST['usuario']
    password = request.POST['contrasena']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        request.user.message_set.create(message="Lo sentimos, no se encuentra registrado en nuestro sistema")
        return HttpResponseRedirect("/")
    else:
        if user.is_active:
            auth.login(request, user)   
            return HttpResponseRedirect("/")
        else:        
            request.user.message_set.create(message="Lo sentimos, usted se encuentra temporalmente desabilitado")
            return HttpResponseRedirect("/")

def logout(request):
    auth.logout(request)    
    return HttpResponseRedirect("/")