# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                       # incorporo para poder acceder a archivos estaticos
from django.conf import settings                                                    # incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                   
from django.contrib.auth.models import Group
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
    datos = {}
    return redireccionar('index.html', solicitud, datos)

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

@login_required
def actulizarPerfil(solicitud):
    if comprobarPermisos(solicitud):
        if solicitud.session['grupoUsuarioid'] == 3:
            usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        else:
            usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
        usuario.direccion = solicitud.POST['direccion']
        usuario.lugar_residencia = solicitud.POST['lugar']
        usuario.telefono = solicitud.POST['fijo']
        usuario.movil = solicitud.POST['celular']
        usuario.email = solicitud.POST['email']
        usuario.web = solicitud.POST['web'] 
        usuario.save()  
        solicitud.user.message_set.create(message="Los datos fueron guardados exitosamente.")    
        return HttpResponseRedirect("/perfil/")
    else:
        return logout(solicitud) 

@login_required
def contrasena(solicitud):
    if comprobarPermisos(solicitud):
        return redireccionar('contrasena.html', solicitud, {})
    else:
        return logout(solicitud)

@login_required
def actulizarContrasena(solicitud):
    if comprobarPermisos(solicitud):
        if solicitud.user.check_password(solicitud.POST['actualPass']):
            solicitud.user.set_password(solicitud.POST['nuevoPass'])
            solicitud.user.save()
            solicitud.user.message_set.create(message="La contraseña fue cambiada.")
            return HttpResponseRedirect("/contrasena/")
        else:        
            solicitud.user.message_set.create(message="Por favor digite nuevamente su contraseña")
            return HttpResponseRedirect("/contrasena/")
    else:
        return logout(solicitud) 

def login(solicitud):
    username = solicitud.POST['usuario']
    password = solicitud.POST['contrasena']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        solicitud.session['msg_error'] = 'Lo sentimos, no se pudo iniciar sesión compruebe que su nombre de usuario y contraseña sean los correctos.'
    else:
        if user.is_active:
            auth.login(solicitud, user)
            resultado = buscarPerfil(solicitud)    
            if resultado[0]['resultado'] == True:        
                solicitud.session['grupoUsuarioid'] = resultado[0]['grupoUsuarioid']
            else:
                auth.logout(solicitud)
                solicitud.session['msg_error'] = 'Lo sentimos, el sistema es de uso exclusivo de docente y estudiantes.'                    
        else:
            solicitud.session['msg_error'] = 'Lo sentimos, usted se encuentra temporalmente inabilitado para acceder a nuestro sistema'
    return HttpResponseRedirect("/")

def logout(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        del solicitud.session['grupoUsuarioid']
    if 'msg_error' in solicitud.session:
        solicitud.session['msg_error']
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")