# -*- coding: utf-8 -*-
from django.core.context_processors import csrf
from datetime import datetime, timedelta, date
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.static import Context, HttpResponseRedirect                       # incorporo para poder acceder a archivos estaticos
from django.conf import settings                                                    # incopora para poder acceder a los valores creados en el settings
from django.contrib import auth                                   
from django.contrib.auth.models import Group, User
from academico.models import Profesor, Estudiante, TipoDocumento, Genero, Estrato, Institucion, MatriculaPrograma, MatriculaCiclo
from financiero.models import MatriculaFinanciera, Ciclo, InscripcionPrograma, Letra
from django.contrib.auth.decorators import login_required                           # permite usar @login_requerid
from academico.views import cicloNuevo

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
    cant = 0
    intituciones = Institucion.objects.all()
    for resultado in intituciones:
        institucion = resultado
        cant = cant + 1
    if cant > 0:    
        variables = {
            'user': solicitud.user,
            'titulo': institucion.nombre,
            'saludo': institucion.saludo,
            'titulo_pagina': u"Sistema de Información Académica | " + institucion.nombre,
            'path': settings.MEDIA_URL,
        }
    else:
        variables = {
            'user': solicitud.user, 
            'titulo': 'Claro',
            'saludo': '',
            'titulo_pagina': u"Sistema de Información Académica | Claro",
            'path': settings.MEDIA_URL,
        }    
    llaves = datos.keys()
    for indice in range(0,len(llaves)):
        variables[llaves[indice]] = datos[llaves[indice]]
    variables =  Context(variables)
    return render_to_response(plantilla, variables, context_instance=RequestContext(solicitud))

def buscarMatriculaProgramasEstudiante(solicitud):
    hoy = date.today()
    usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
    return MatriculaPrograma.objects.filter(estudiante = usuario.id, fecha_inscripcion__lte = hoy, fecha_vencimiento__gte = hoy)


def buscarInscribirMaterias(solicitud):
    inscribir = 0
    hoy = date.today()
    inscripcion = Ciclo.objects.filter(fecha_inicio_inscripcion__lte = hoy, fecha_fin_inscripcion__gte = hoy)
    if len(inscripcion)>0:
        inscribir = 1
    return inscribir
 
 
def pazySalvo(solicitud):
    mora = False
    hoy = date.today()
    matProgramas = buscarMatriculaProgramasEstudiante(solicitud)
    for matPrograma in matProgramas:       
        matCiclos = MatriculaCiclo.objects.filter(matricula_programa = matPrograma.id)
        for matCiclo in matCiclos:
            ciclo = Ciclo.objects.get(id = matCiclo.ciclo_id) 
            insPros = InscripcionPrograma.objects.filter(matricula_programa = matPrograma.id)
            for insPro in insPros:
                matFinans = MatriculaFinanciera.objects.filter(inscripcion_programa = insPro, ciclo = ciclo.id)
                for matFinan in matFinans:
                    letras = Letra.objects.filter(matricula_financiera = matFinan)
                    if len(letras) > 0:
                        cantidad = 0
                        fechaVencimiento = matFinan.fecha_expedicion
                        for letra in letras:
                            if letra.cancelada == True:
                                cantidad = cantidad + 1
                            else:
                                if letra.fecha_expedicion >= date.today() or  letra.fecha_vencimiento >= hoy:
                                    cantidad = cantidad + 1
                                else:
                                    if matFinan.fecha_expedicion == fechaVencimiento:
                                        fechaVencimiento = letra.fecha_vencimiento
                                    if fechaVencimiento > letra.fecha_vencimiento:
                                        fechaVencimiento = letra.fecha_vencimiento                                   
                        if cantidad != len(letras):
                            mora = True
                            diasMora = hoy - fechaVencimiento
                            if 'diasMora' in solicitud.session and solicitud.session['diasMora'] < diasMora.days:
                                solicitud.session['diasMora'] = diasMora.days
                            else:
                                solicitud.session['diasMora'] = diasMora.days
                    else:
                        if matFinan.paz_y_salvo == False:
                            mora = True
                            diasMora = hoy - matFinan.fecha_expedicion
                            if 'diasMora' in solicitud.session and solicitud.session['diasMora'] < diasMora.days:
                                solicitud.session['diasMora'] = diasMora.days
                            else:
                                solicitud.session['diasMora'] = diasMora.days                       
    solicitud.session['mora'] = mora
    
def indice(solicitud):
    return redireccionar('index.html', solicitud, {})

@login_required
def perfil(solicitud):
    if comprobarPermisos(solicitud):
        if solicitud.session['grupoUsuarioid'] == 3:
            usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        else:
            usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
        if usuario.foto == '':
            foto = 'images/perfil.jpg'
        else:
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
        c = {}
        c.update(csrf(solicitud.POST.get('csrfmiddlewaretoken')))     
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
    
def fotoPerfil(solicitud):
    if comprobarPermisos(solicitud):
        if solicitud.session['grupoUsuarioid'] == 3:
            usuario = Profesor.objects.get(id_usuario = solicitud.user.id)
        else:
            usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
        if solicitud.method == 'POST':
            usuario.foto = solicitud.FILES['foto']
            usuario.save() 
            return HttpResponseRedirect("../")
    else:
        return HttpResponse()   

@login_required
def contrasena(solicitud):
    if comprobarPermisos(solicitud):
        return redireccionar('contrasena.html', solicitud, {})
    else:
        return logout(solicitud)

def actulizarContrasena(solicitud):
    if solicitud.POST:
        c = {}
        c.update(csrf(solicitud.POST.get('csrfmiddlewaretoken')))       
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
        solicitud.session['msg_error'] = 'Usuario/contraseña incorrecto.'
    else:
        if user.is_active:
            auth.login(solicitud, user)
            resultado = buscarPerfil(solicitud)    
            if resultado[0]['resultado'] == True:        
                solicitud.session['grupoUsuarioid'] = resultado[0]['grupoUsuarioid']
                if solicitud.session['grupoUsuarioid'] == 4:
                    pazySalvo(solicitud)
                solicitud.session['inscribir'] = buscarInscribirMaterias(solicitud)
                intituciones = Institucion.objects.all()
                institucion = {}
                for resultado in intituciones:
                    institucion = resultado
                if institucion.control_acudiente == True:
                    if solicitud.session['grupoUsuarioid'] == 3:
                        solicitud.session['control'] = 0
                    if solicitud.session['grupoUsuarioid'] == 4:
                        usuario = Estudiante.objects.get(id_usuario = solicitud.user.id)
                        if usuario.fecha_nacimiento is None:
                            solicitud.session['control'] = 1
                        else:
                            hoy = datetime.now()
                            edad = hoy.year - usuario.fecha_nacimiento.year
                            if edad == 18:
                                if hoy.month < usuario.fecha_nacimiento.month:
                                    solicitud.session['control'] = 1
                                else:
                                    if hoy.month > usuario.fecha_nacimiento.month:
                                        solicitud.session['control'] = 0
                                    else:
                                        if hoy.day < usuario.fecha_nacimiento.day:
                                            solicitud.session['control'] = 1
                                        else:
                                            solicitud.session['control'] = 0
                            else:
                                if edad > 18:
                                    solicitud.session['control'] = 0
                                else:
                                    solicitud.session['control'] = 1
                else:
                    solicitud.session['control'] = 0
            else:
                auth.logout(solicitud)
                solicitud.session['msg_error'] = 'Acceso denegado'                    
        else:
            solicitud.session['msg_error'] = 'Acceso denegado'
    return HttpResponseRedirect("/")

def logout(solicitud):
    if 'grupoUsuarioid' in solicitud.session:
        del solicitud.session['grupoUsuarioid']
    if 'mora' in solicitud.session:
        del solicitud.session['mora']
    if 'diasMora' in solicitud.session:
        del solicitud.session['diasMora'] 
    if 'msg_error' in solicitud.session:
        del solicitud.session['msg_error']
    auth.logout(solicitud)    
    return HttpResponseRedirect("/")