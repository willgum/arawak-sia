# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                       # se incorporo para poder acceder a archivos estaticos
from django.conf import settings                                                    # se incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                   
from django.contrib.auth.models import Group
from academico.models import Profesor, Estudiante, TipoDocumento, Genero, Estrato
from django.contrib.auth.decorators import login_required                           # me permite usar eö @login_requerid

def comprobarPerfil(solicitud):
    respuesta = [] 
    grupos = solicitud.user.groups.all()    
    if len(grupos) > 0:
        respuesta.append({'resultado':True, 'grupos':grupos})
    else:
        respuesta.append({'resultado':False})    
    return respuesta

def buscarPerfil(grupos):
    respuesta = []       
    for grupo in grupos:
        grupoUsuario = Group.objects.get(name = grupo)    
    if grupoUsuario.id == 3 or grupoUsuario.id == 4:
        respuesta.append({'resultado':True, 'grupoUsuarioid':grupoUsuario.id})        
    else:
        respuesta.append({'resultado':False})    
    return respuesta

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
    datos = {}
    resultado = comprobarPerfil(solicitud)    
    if resultado[0]['resultado'] == True:
        resultado = buscarPerfil(resultado[0]['grupos'])
        if resultado[0]['resultado'] == True:
            if resultado[0]['grupoUsuarioid'] == 3:
                usuario = Profesor.objects.get(documento = solicitud.user)
            else:
                usuario = Estudiante.objects.get(documento = solicitud.user)            
            datos = {'usuario': usuario,
                     'tipoDocumento': TipoDocumento.objects.get(codigo = usuario.tipo_documento_id),
                     'genero': Genero.objects.get(codigo = usuario.genero_id),
                     'estratos': Estrato.objects}
        else:            
            datos = {'msg_error': "Lo sentimos, no se puede tener acceso a su perfil."}
    else:
        datos = {'msg_error': "Lo sentimos, no se puede tener acceso a su perfil."}
    return redireccionar('perfil.html', solicitud, datos)

@login_required
def actulizarPerfil(solicitud):
    resultado = comprobarPerfil(solicitud)    
    if resultado[0]['resultado'] == True:
        resultado = buscarPerfil(resultado[0]['grupos'])        
        if resultado[0]['resultado'] == True:            
            if resultado[0]['grupoUsuarioid'] == 3:
                usuario = Profesor.objects.get(documento = solicitud.user)
            else:
                usuario = Estudiante.objects.get(documento = solicitud.user)
    usuario.direccion = solicitud.POST['direccion']
    usuario.lugar_residencia = solicitud.POST['lugar']
    usuario.telefono = solicitud.POST['fijo']
    usuario.movil = solicitud.POST['celular']
    usuario.email = solicitud.POST['email']
    usuario.web = solicitud.POST['web'] 
    usuario.save()  
    solicitud.user.message_set.create(message="Los datos fueron guardados exitosamente.")    
    return HttpResponseRedirect("/perfil/")

@login_required
def contrasena(solicitud):
    datos = {}
    return redireccionar('contrasena.html', solicitud, datos)

@login_required
def actulizarContrasena(solicitud):
    if solicitud.user.check_password(solicitud.POST['actualPass']):
        solicitud.user.set_password(solicitud.POST['nuevoPass'])
        solicitud.user.save()
        solicitud.user.message_set.create(message="La contraseña fue cambiada.")
        return HttpResponseRedirect("/contrasena/")
    else:        
        solicitud.user.message_set.create(message="Por favor digite nuevamente su contraseña")
        return HttpResponseRedirect("/contrasena/")

def login(solicitud):
    datos = {}
    username = solicitud.POST['usuario']
    password = solicitud.POST['contrasena']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        datos = {'msg_error': "Lo sentimos, no se encuentra registrado en nuestro sistema."}
    else:
        if user.is_active:
            auth.login(solicitud, user)
        else:        
            datos = {'msg_error': "Lo sentimos, no se pudo iniciar sesión compruebe que su nombre de usuario y contraseña se encuentren bien diligenciados."}
    return redireccionar('index.html', solicitud, datos)

def logout(solicitud):
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")