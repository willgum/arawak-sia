# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                       # incorporo para poder acceder a archivos estaticos
from django.conf import settings                                                    # incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                   
from django.contrib.auth.models import Group, User
from academico.models import Profesor, Estudiante, TipoDocumento, Genero, Estrato
from django.contrib.auth.decorators import login_required                           # permite usar @login_requerid

def buscarPerfil(solicitud):
    respuesta = [] 
    grupos = solicitud.user.groups.all()    
    if len(grupos) > 0:
        for grupo in grupos:
            grupoUsuario = Group.objects.get(name = grupo)    
        if grupoUsuario.id == 3 or grupoUsuario.id == 4:
            respuesta.append({'resultado':True, 'grupoUsuarioid':grupoUsuario.id})        
        else:
            respuesta.append({'resultado':False})
    else:
        respuesta.append({'resultado':False})    
    return respuesta

def comprobarPermisos(solicitud):
    if 'grupoUsuarioid' in solicitud.session: 
        sesion = Session.objects.get(session_key = solicitud.session.session_key)
        if  datetime.now() <= sesion.expire_date:
            sesion.expire_date = datetime.now() + timedelta(minutes=10)
            sesion.save()
        if solicitud.session['grupoUsuarioid'] == 3:
            return True
        else:
            if solicitud.session['grupoUsuarioid'] == 4:
                return True
            else:
                return False
    else:
        return False

def redireccionar(plantilla, solicitud, datos):
    variables = {
        'user': solicitud.user, 
        'titulo': '.: SIA - Sistema de Información Académica :.',
        'titulo_pagina': '.: SIA - Sistema de Información Académica :.',
        'path': settings.MEDIA_URL,
    }
    llaves = datos.keys()
    for indice in range(0,len(llaves)):
        variables[llaves[indice]] = datos[llaves[indice]]
    variables =  Context(variables)
    return render_to_response(plantilla, variables, context_instance=RequestContext(solicitud))
        
def indice(solicitud):
    return redireccionar('index.html', solicitud, {})

@login_required
def perfil(solicitud):
    if comprobarPermisos(solicitud):
        if solicitud.session['grupoUsuarioid'] == 3:
            usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        else:
            usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
        foto = str(usuario.foto).replace('original','thumbnail')
        datos = {'usuario': usuario,
                 'foto': foto,
                 'tipoDocumento': TipoDocumento.objects.get(codigo = usuario.tipo_documento_id),
                 'genero': Genero.objects.get(codigo = usuario.genero_id),
                 'estratos': Estrato.objects} 
        return redireccionar('perfil.html', solicitud, datos)
    else:
        return logout(solicitud)    

def actulizarPerfil(solicitud):
    if solicitud.POST:
        idUsuario = solicitud.POST.get('idUsuario')
        perfil = solicitud.POST.get('perfil')
        campo = solicitud.POST.get('campo')
        valor = solicitud.POST.get('valor') 
        if perfil == str(3):
            usuario = Profesor.objects.get(id_usuario = idUsuario)
        else:
            usuario = Estudiante.objects.get(id_usuario = idUsuario)
        if campo == 'direccion': 
            usuario.direccion = valor
        if campo == 'lugar': 
            usuario.lugar_residencia = valor
        if campo == 'fijo': 
            usuario.telefono = valor
        if campo == 'celular': 
            usuario.movil = valor
        if campo == 'email': 
            usuario.email = valor
        if campo == 'web': 
            usuario.web = valor
        usuario.save() 
        return HttpResponse()

@login_required
def contrasena(solicitud):
    if comprobarPermisos(solicitud):
        return redireccionar('contrasena.html', solicitud, {})
    else:
        return logout(solicitud)

def actulizarContrasena(solicitud):
    if solicitud.POST:
        idUsuario = solicitud.POST.get('idUsuario')
        actualPass = solicitud.POST.get('actualPass')
        nuevoPass = solicitud.POST.get('nuevoPass')
        usuario = User.objects.get(id = idUsuario)
        if usuario.check_password(actualPass):            
            usuario.set_password(nuevoPass)
            usuario.save()
            return HttpResponse("Su contraseña fue actualizada")
        else:        
            return HttpResponse("Por favor digite nuevamente su contraseña")

def login(solicitud):
    username = solicitud.POST['usuario']
    password = solicitud.POST['contrasena']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        solicitud.session['msg_error'] = 'Nombre de usuario y/o contraseña incorrectos.'
    else:
        if user.is_active:
            auth.login(solicitud, user)
            resultado = buscarPerfil(solicitud)    
            if resultado[0]['resultado'] == True:        
                solicitud.session['grupoUsuarioid'] = resultado[0]['grupoUsuarioid']
            else:
                auth.logout(solicitud)
                solicitud.session['msg_error'] = 'Acceso denegado'                    
        else:
            solicitud.session['msg_error'] = 'Acceso denegado'
    return HttpResponseRedirect("/")

def logout(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        del solicitud.session['grupoUsuarioid']
    if 'msg_error' in solicitud.session:
        solicitud.session['msg_error']
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")