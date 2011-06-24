# -*- coding: utf-8 -*-
import datetime
import Image
import os
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings 
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.forms import ModelForm, TextInput

#NOTA_MIN = 0.0
#NOTA_MAX = 5.0
#NOTA_APR = 3.5

MINI_WIDTH = 80
MINI_HEIGHT = 100
THUMB_WIDTH = 120
THUMB_HEIGHT = 150

TipoValoracion = (
    ('1', 'Numérica'),
    ('2', 'Conceptual'),
    ('3', 'Horas'),
)

def crear_usuario(nombre1, nombre2, apellido1, apellido2):
    tmp_nombre2 = ""
    tmp_apellido2 = ""
    repetido = True
    total_usuarios = 0
    num_usuario = ""
    
    if len(nombre2) > 0:
        tmp_nombre2 = nombre2[0]
        
    if len(apellido2.strip()) > 0:
        tmp_apellido2 = apellido2[0]
        
    tmp = "%s%s%s%s" % (nombre1[0], tmp_nombre2, apellido1, tmp_apellido2)
    usuario = normalizar_usuario(tmp)
    
    while repetido == True:
        tmp_usuario = "%s%s" % (usuario, num_usuario)
        if len(User.objects.filter(username=tmp_usuario)) > 0:
            total_usuarios = total_usuarios + 1
            num_usuario = chr(96 + total_usuarios)
        else:
            repetido = False
            usuario = tmp_usuario
            
    return usuario

def normalizar_usuario(cadena):
    # Remueve caracteres especiales y espacios de los nombres de usuario.
    cadena = cadena.lower()
    cadena = cadena.replace(u"á", "a")
    cadena = cadena.replace(u"é", "e")
    cadena = cadena.replace(u"í", "i")
    cadena = cadena.replace(u"ó", "o")
    cadena = cadena.replace(u"ú", "u")
    cadena = cadena.replace(u"ü", "u")
    cadena = cadena.replace(u"ñ", "n")
    cadena = cadena.replace(" ", "")
#    cadena = cadena.replace(" ", "_")
    return cadena

def normalizar_cadena(cadena):
    # Remueve caracteres especiales para evitar error utf8.
    cadena = cadena.replace(u"á", "a")
    cadena = cadena.replace(u"é", "e")
    cadena = cadena.replace(u"í", "i")
    cadena = cadena.replace(u"ó", "o")
    cadena = cadena.replace(u"ú", "u")
    cadena = cadena.replace(u"ü", "u")
    cadena = cadena.replace(u"ñ", "n")
    
    cadena = cadena.replace(u"Á", "A")
    cadena = cadena.replace(u"É", "E")
    cadena = cadena.replace(u"Í", "I")
    cadena = cadena.replace(u"Ó", "O")
    cadena = cadena.replace(u"Ú", "U")
    cadena = cadena.replace(u"Ü", "U")
    cadena = cadena.replace(u"Ñ", "N")
    return cadena


class Sisben (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre

class Etnia (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre

class TipoComportamiento (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre

class Estrato (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre

class EstadoInscripcion (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre

class TipoDocumento (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre

class Genero (models.Model):
    codigo = models.CharField(max_length = 1)
    nombre = models.CharField(max_length = 20)
    
    def __unicode__(self):
        return self.nombre
    
class GrupoSanguineo (models.Model):
    nombre = models.CharField(max_length = 15)
    
    def __unicode__(self):
        return self.nombre

class TipoReferencia (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre


class Discapacidad (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre

class Jornada (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre

class Periodicidad(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre

class Dia(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre

class TipoSalon(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre

class TipoEstudio(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre


class TipoAprobacion(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre
    
    def get_codigo(self):
        return self.codigo

    
class TipoNotaConceptual(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre
    
    def get_codigo(self):
        return self.codigo
    
    class Meta:
        verbose_name_plural = 'Tipo notas conceptuales'


class TipoPrograma(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    nota_minima = models.FloatField(blank=True, null=True, default=0)
    nota_maxima = models.FloatField(blank=True, null=True, default=0)
    nota_aprobacion = models.FloatField(blank=True, null=True, default=0)
    
    def __unicode__(self):
        return self.nombre


class TipoFuncionario (models.Model):
    codigo = models.CharField(max_length = 3)
    nombre = models.CharField(max_length = 50)
    
    def __unicode__(self):
        return self.nombre


#    TODO: implementar opción para validar notas permitidas
#def validar_nota(nota):
#    raise ValidationError("%s no es una nota válida" % nota)
#        if nota < NOTA_MIN or nota > NOTA_MAX:
#            raise ValidationError("%s no es una nota válida" % nota)
        
def validar_porcentaje(porcentaje):
        if porcentaje < 1 or porcentaje > 100:
            raise ValidationError(u"%s no es una porcentaje válido" % porcentaje)

def validar_digito(digito):
    if not digito.isdigit():
        raise ValidationError(u"No es dígito válido")

def validar_numerico(cifra):
    for c in cifra:
        if not c.isdigit():
            raise ValidationError(u'No es valor numérico válido')

#    scale: Función para escalar una imágen a un with y height dados
def scale(fname, width, height, fname_scaled):
    if os.path.exists(fname):
        img = Image.open(fname)
        
        new_height = width * img.size[1] / img.size[0]
        new_width = height * img.size[0] / img.size[1]
        
        if height - new_height > 0:
            new_height = height
            new_width = new_height * img.size[0] / img.size[1]
        elif width - new_width > 0:
            new_width = width
            new_height = width * img.size[1] / img.size[0]
        
        out = img.resize((new_width, new_height))
        box = ((new_width/2 - width/2), (new_height/2 - height/2), (new_width/2 + width/2), (new_height/2 + height/2))
        out = out.crop(box)
        out.save(fname_scaled, "JPEG")


class CustomStorage(FileSystemStorage):
#    En caso de que la imagen exista, la borra para ingresarla de nuevo
#    Django por defecto no sobreescribe la original, 
#    sino que agrega un _# al final del nombre del archivo.
    def _open(self, name, mode='rb'):
        return File(open(self.path(name), mode))

    def _save(self, name, content):
        # here, you should implement how the file is to be saved
        # like on other machines or something, and return the name of the file.
        fs = FileSystemStorage()
        name = fs._save(name, content)
        return name

    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name
    
    
class Ciclo(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=8, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __unicode__(self):
        return self.codigo
    
    def cortes(self):
        return len(Corte.objects.filter(ciclo=self))
    
    def cicloActual(self):
        hoy = datetime.date.today() 
        return self.fecha_inicio <= hoy <= self.fecha_fin
         
        
class CicloForm(ModelForm):
    class Meta:
        model = Ciclo
        widgets = {'fecha_inicio': TextInput(attrs={'class':'vDateField'}),
                   'fecha_fin': TextInput(attrs={'class':'vDateField'})}
        
class Profesor(models.Model):
    # Informacion personal
#    custom_store = CustomStorage()
    
    nombre1 = models.CharField(max_length=50, verbose_name='Primer nombre')
    nombre2= models.CharField(max_length=50, verbose_name='Segundo nombre', blank=True)
    apellido1 = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido2 = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True)
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True, default=1) 
    documento = models.CharField(max_length=12, unique = True, validators=[validar_numerico])
    genero = models.ForeignKey(Genero, blank=True, null=True, default=1) 
    grupo_sanguineo = models.ForeignKey(GrupoSanguineo, verbose_name='Grupo sanguíneo', blank=True, null=True, default=1)
    lugar_expedicion = models.CharField(verbose_name='Lugar expedición', max_length=200, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(blank=True, max_length=200)
    foto = models.ImageField(storage=CustomStorage(), upload_to='imagenes/original/', blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, blank=True)
    # Informacion de contacto
    direccion = models.CharField(verbose_name='Dirección', max_length=200, blank=True)
    lugar_residencia = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=20, blank=True)
    movil = models.CharField(verbose_name='Móvil', max_length=20, blank=True)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)
    id_usuario = models.IntegerField(blank=True)
    
#    Sobreescribir la función guardar para crear usuario
#    Guardar información de acceso a la tabla de usuarios de DJANGO
#    Grupo 3 corresponde en la base de datos con un perfil profesor
    
    def save(self, *args, **kwargs):
        existe_foto = False
        self.nombre1 = self.nombre1.strip()
        self.nombre2 = self.nombre2.strip()
        self.apellido1 = self.apellido1.strip()
        self.apellido2 = self.apellido2.strip()
        
        if self.foto.name != "":
            tmp_foto = self.documento + "c.jpg"
            self.foto.name = "imagenes/original/" + tmp_foto
            existe_foto = True
        
        try:
                user = User.objects.get(id=self.id_usuario)
        except User.DoesNotExist:
                usuario = crear_usuario(self.nombre1, self.nombre2, self.apellido1, self.apellido2)
                user = User.objects.create_user(usuario, self.email, self.documento)
                user.groups.add(3);
                user.save()
                
        user.is_staff = False
        user.first_name = self.nombre1
        user.last_name = self.apellido1
        user.email = self.email
        user.save()
        self.id_usuario = user.id
        
        super(Profesor, self).save(*args, **kwargs)
         
#        OPCIÓN PARA CARGAR FOTO EN TAMAÑO ORIGINAL, MINI Y THUMNAIL
        if existe_foto == True:
            foto_org = settings.MEDIA_ROOT + "imagenes/original/" + tmp_foto
            foto_min = settings.MEDIA_ROOT + "imagenes/mini/" + tmp_foto
            foto_thu = settings.MEDIA_ROOT + "imagenes/thumbnail/" + tmp_foto
            scale(foto_org, THUMB_WIDTH, THUMB_HEIGHT, foto_thu)
            scale(foto_org, MINI_WIDTH, MINI_HEIGHT, foto_min)
 
    def nombre(self):
        return "%s %s %s %s" %(self.nombre1, self.nombre2, self.apellido1, self.apellido2) 
    
    def usuario(self):
        user = User.objects.get(id=self.id_usuario)
        return user
        
    def __unicode__(self):
        return u"%s %s %s %s" %(self.apellido1, self.apellido2, self.nombre1, self.nombre2)
#        return "%s %s" % (self.nombre1, self.apellido1) 
    
    class Meta:
        verbose_name_plural = 'profesores'


class ProfesorExperiencia(models.Model):
    profesor = models.ForeignKey(Profesor, blank=True, null=True, default=1)
    cargo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    actualmente = models.BooleanField(help_text='Indica si trabaja actualmente en la empresa.')
    
    def __unicode__(self):
        return self.cargo
    
    class Meta:
        verbose_name_plural = 'Experiencia profesional'
    
class Salon(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=12, unique=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    capacidad = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    tipo_salon = models.ForeignKey(TipoSalon, blank=True, default=1)
    
    def __unicode__(self):
        return self.codigo
    
    class Meta:
        verbose_name_plural = 'salones'


class Programa(models.Model):
    
    # Informacion general
    tipo_programa = models.ForeignKey(TipoPrograma, blank=True, null=True, default=1)
    codigo = models.CharField(verbose_name='Código', max_length=4, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, help_text='Título otorgado al finalizar el programa.', blank=True)
    resolucion = models.CharField(verbose_name='Resolución', max_length=200, help_text="Acto administrativo que valida este programa.", blank=True)
    snies = models.CharField(verbose_name='SNIES', max_length=200, help_text="Código Sistema Nacional de Información de la Educación Superior.", blank=True)
    
    # Horario
    periodicidad = models.ForeignKey(Periodicidad, blank=True, null=True, default=2) 
    duracion = models.SmallIntegerField(verbose_name='Duración', blank=True, null=True, validators=[MinValueValidator(0)])
    jornada = models.ForeignKey(Jornada, blank=True, null=True, default=1)
    
    # Informacion adicional
    horas_bienestar = models.IntegerField(help_text="Número de horas de bienestar necesaria para aprobar el programa.", blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    aptitudes = models.TextField(max_length=200, help_text="Aptitudes requeridas para los aspirantes.", blank=True)
    perfil_profesional = models.TextField(max_length=200, help_text="Perfil profesional del egresado.", blank=True)
    funciones = models.TextField(max_length=200,help_text="Funciones en las que se puede desempeñar el egresado.", blank=True)
 
    def materias(self):
        return len(Materia.objects.filter(programa=self))
    
    def __unicode__(self):
        return self.nombre
    
    def abreviatura(self):
        return self.nombre[0:5] + " ... " + self.nombre[-5:]
    
    def notaMin(self):
        return self.tipo_programa.nota_minima
    
    def notaMax(self):
        return self.tipo_programa.nota_maxima


class Estudiante(models.Model):
    
    # Identificacion
    nombre1 = models.CharField(max_length=50, verbose_name='Primer nombre')
    nombre2= models.CharField(max_length=50, verbose_name='Segundo nombre', blank=True)
    apellido1 = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido2 = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True)
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True, default=1) 
    documento = models.CharField(max_length=12, unique = True, validators=[validar_numerico])
    lugar_expedicion = models.CharField(max_length=200, verbose_name='Lugar expedición', blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.ForeignKey(Genero, blank=True, null=True, default=1) 
    grupo_sanguineo = models.ForeignKey(GrupoSanguineo, verbose_name='Grupo sanguíneo', blank=True, null=True, default=1)
    lugar_nacimiento = models.CharField(max_length=200, blank=True)
    
    # Requisitos
    fotocopia_documento = models.ImageField(storage=CustomStorage(), upload_to='imagenes/original/', blank=True)
    fotocopia_diploma = models.ImageField(storage=CustomStorage(), upload_to='imagenes/original/', blank=True)
    foto = models.ImageField(storage=CustomStorage(), upload_to='imagenes/original/', blank=True)
    
    # Informacion de contacto
    direccion = models.CharField( verbose_name='Dirección', max_length=200, blank=True)
    lugar_residencia = models.CharField(max_length=200, blank=True)
    estrato = models.ForeignKey(Estrato, blank=True, null=True, default=4)
    telefono = models.CharField(verbose_name='Teléfono', max_length=20, blank=True)
    movil = models.CharField(verbose_name='Móvil', max_length=20, blank=True)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)
    id_usuario = models.IntegerField(blank=True)
    
    # Informacion adicional
    sisben = models.ForeignKey(Sisben, blank=True, default=1, null=True)
    discapacidad = models.ForeignKey(Discapacidad, blank=True, default=1, null=True)
    etnia = models.ForeignKey(Etnia, default=1, blank=True, null=True)
    
    def nombre(self):
        return u"%s %s %s %s" %(self.apellido1, self.apellido2, self.nombre1, self.nombre2)
    
#       Sobreescribir la función guardar para crear usuario
#       Guardar información de acceso a la tabla de usuarios de DJANGO
#       Grupo 4 corresponde en la base de datos con un perfil estudiante

    def save(self, *args, **kwargs):
        existe_foto = False
        existe_diploma = False
        existe_documento = False
        self.nombre1 = self.nombre1.strip()
        self.nombre2 = self.nombre2.strip()
        self.apellido1 = self.apellido1.strip()
        self.apellido2 = self.apellido2.strip()
        
        if self.fotocopia_documento.name != "":
            existe_documento = True
            tmp_documento = self.documento + "a.jpg"
            self.fotocopia_documento.name = "imagenes/original/" + tmp_documento
        if self.fotocopia_diploma.name != "":
            existe_diploma = True
            tmp_diploma = self.documento + "b.jpg"
            self.fotocopia_diploma.name = "imagenes/original/" + tmp_diploma
        if self.foto.name != "":
            existe_foto = True
            tmp_foto = self.documento + "c.jpg"
            self.foto.name = "imagenes/original/" + tmp_foto
            
        try:
            user = User.objects.get(id=self.id_usuario)
        except User.DoesNotExist:
            usuario = crear_usuario(self.nombre1, self.nombre2, self.apellido1, self.apellido2)
            user = User.objects.create_user(usuario, self.email, self.documento)
            user.groups.add(4);
            user.save()
                
        user.is_staff = False
        user.first_name = self.nombre1
        user.last_name = self.apellido1
        user.email = self.email
        user.save()
        self.id_usuario = user.id
        
        super(Estudiante, self).save(*args, **kwargs)
        
#        OPCIÓN PARA CARGAR FOTO EN TAMAÑO ORIGINAL, MINI Y THUMNAIL
        if existe_foto == True:
            foto_org = settings.MEDIA_ROOT + "imagenes/original/" + tmp_foto
            foto_min = settings.MEDIA_ROOT + "imagenes/mini/" + tmp_foto
            foto_thu = settings.MEDIA_ROOT + "imagenes/thumbnail/" + tmp_foto
            scale(foto_org, THUMB_WIDTH, THUMB_HEIGHT, foto_thu)
            scale(foto_org, MINI_WIDTH, MINI_HEIGHT, foto_min)
        
#        OPCIÓN PARA CARGAR DIPLOMA EN TAMAÑO ORIGINAL, MINI Y THUMNAIL
        if existe_diploma == True:
            diploma_org = settings.MEDIA_ROOT + "imagenes/original/" + tmp_diploma
            diploma_min = settings.MEDIA_ROOT + "imagenes/mini/" + tmp_diploma
            diploma_thu = settings.MEDIA_ROOT + "imagenes/thumbnail/" + tmp_diploma
            scale(diploma_org, THUMB_WIDTH, THUMB_HEIGHT, diploma_thu)
            scale(diploma_org, MINI_WIDTH, MINI_HEIGHT, diploma_min)

#        OPCIÓN PARA CARGAR DOCUMENTO EN TAMAÑO ORIGINAL, MINI Y THUMNAIL
        if existe_documento == True:
            documento_org = settings.MEDIA_ROOT + "imagenes/original/" + tmp_documento
            documento_min = settings.MEDIA_ROOT + "imagenes/mini/" + tmp_documento
            documento_thu = settings.MEDIA_ROOT + "imagenes/thumbnail/" + tmp_documento
            scale(documento_org, THUMB_WIDTH, THUMB_HEIGHT, documento_thu)
            scale(documento_org, MINI_WIDTH, MINI_HEIGHT, documento_min)
    
    def usuario(self):
        user = User.objects.get(id=self.id_usuario)
        return user
    
    def __unicode__(self):
        return u"%s %s %s %s" %(self.apellido1, self.apellido2, self.nombre1, self.nombre2)
#        return self.documento


class EstudioComplementario(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    tipo_estudio = models.ForeignKey(TipoEstudio, blank=True, null=True, default=1) 
    institucion = models.CharField( verbose_name='Institución', max_length=200,  blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, blank=True)
    fecha_graduacion = models.DateField(verbose_name='Fecha graduación', blank=True, null=True)


class Referencia(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    tipo_referencia = models.ForeignKey(TipoReferencia, blank=True, null=True, default=1) 
    nombre = models.CharField(max_length=200, blank=True)
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True, default=1)
    documento = models.CharField(max_length=12, blank=True)
    direccion = models.CharField(verbose_name='Dirección', max_length=200, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=20,  blank=True)


class MatriculaPrograma(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    fecha_inscripcion = models.DateField(verbose_name='Fecha inscripción')
    programa = models.ForeignKey(Programa)
    codigo = models.CharField(verbose_name='Código', max_length=12, unique = True, blank=True)
    estado = models.ForeignKey(EstadoInscripcion, blank=True, null=True, default=1)
    fecha_vencimiento = models.DateField()
    becado = models.BooleanField(help_text='Indica si el estudiante recibe o no beca.')
    promedio_acumulado = models.FloatField(blank=True, null=True, default=0)
    horas_bienestar = models.IntegerField(help_text="Número de horas de bienestar acumuladas.", blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    
    def nombre_estudiante(self):
        return self.estudiante.nombre()
    
    def nombre_programa(self):
        return u"%s" %(self.programa.nombre)
    
    def abreviatura(self):
        return self.programa.abreviatura()
    
    def usuario(self):
        return u"%s" %(self.estudiante.usuario())
    
    def calculaPromedioAcumulado(self, matricula_programa_id):
        tmp_promedio_ciclo = MatriculaCiclo.objects.filter(matricula_programa = matricula_programa_id)
        tmp_promedio_acumulado = 0.0
        
        for tmp_nota in tmp_promedio_ciclo:
            tmp_promedio_acumulado = tmp_promedio_acumulado + tmp_nota.promedio_ciclo
        
        if len(tmp_promedio_ciclo)>0:
            self.promedio_acumulado = round(tmp_promedio_acumulado/len(tmp_promedio_ciclo), 2)
        else:
            self.promedio_acumulado = 0
        MatriculaPrograma.save(self)
    
    def estudianteActivo(self):
        if self.estado.id==1:  return 1
        else:               return 0
    def estudianteEgresado(self):
        if self.estado.id==2:  return 1
        else:               return 0
    def estudianteExpulsado(self):
        if self.estado.id==3:  return 1
        else:               return 0
    def estudianteRetirado(self):
        if self.estado.id==4:  return 1
        else:               return 0
    def estudianteSuspendido(self):
        if self.estado.id==5:  return 1
        else:               return 0
    def estudiantePendiente(self):
        if self.estado.id==6:  return 1
        else:               return 0
     
#    Asignar automáticamente código de inscripción a estudiante
    def save(self, *args, **kwargs):
        tmp_cod = 1
        q = MatriculaPrograma.objects.filter(codigo__startswith=self.programa.codigo).order_by('-codigo')
        for tmp_q in q:
            tmp_cod = int(tmp_q.codigo.replace(self.programa.codigo, "")) + 1
            break
#        tmp_codigo = "%s" %(MatriculaPrograma.objects.filter(codigo__startswith=self.programa.codigo).count() + 1)
        tmp_codigo = "%s" %(tmp_cod)
        if self.id is None:
            self.codigo = "%s%s" %(self.programa.codigo, tmp_codigo.zfill(5))
            
        super(MatriculaPrograma, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.codigo
    
    class Meta:
        unique_together = ("estudiante", "programa")
        verbose_name = 'Matrícula programa'
        verbose_name_plural = 'Matrícula programas' 


class MatriculaProgramaForm(ModelForm):
    class Meta:
        model = MatriculaPrograma
        
        
class Materia(models.Model):
    programa = models.ForeignKey(Programa)
    requisito = models.ManyToManyField("self", symmetrical=False, blank=True, null=True)
    codigo = models.CharField(max_length=10)
    sufijo = models.CharField(max_length=3, help_text='El sufijo se añade al código del programa y forma el código')
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    creditos = models.IntegerField(help_text='Número de créditos de la materia.', blank=True, null=True)
    periodo = models.SmallIntegerField(help_text='Nivel en el cual se debe ver esta materia.', blank=True, null=True)
    tipo_valoracion = models.CharField(max_length=1, choices=TipoValoracion, blank=True, default='1')
    intensidad_semanal = models.SmallIntegerField(help_text='Número de horas requeridas en la semana.', blank=True, null=True, validators=[MinValueValidator(0)])
    intensidad_ciclo = models.SmallIntegerField(help_text='Número de horas requeridas para dictar la compentencia.', blank=True, null=True, validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ('programa__nombre', 'periodo', 'nombre')
        
    def save(self, *args, **kwargs):
        self.codigo = "%s%s" % (self.programa.codigo, self.sufijo)
        super(Materia, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u"%s | %s" % (
            unicode(self.programa.abreviatura()),
            unicode(self.nombre))
    
    def grupos(self):
        return len(Curso.objects.filter(materia=self))
    
    def idPrograma(self):
        return self.programa.id
    
    def codigoPrograma(self):
        return "%s" % (self.programa.codigo)
    
    def nombrePrograma(self):
        return "%s" % (self.programa.nombre)
        
    def notaMin(self):
        return self.programa.notaMin()
    
    def notaMax(self):
        return self.programa.notaMax()
  
  
class MatriculaCiclo(models.Model):
    fecha_inscripcion = models.DateField()
    matricula_programa = models.ForeignKey(MatriculaPrograma)
    ciclo = models.ForeignKey(Ciclo)
    observaciones = models.TextField(max_length=200, blank=True)
    promedio_ciclo = models.FloatField(blank=True, null=True, default=0)
    
    def __unicode__(self):
        return self.matricula_programa.codigo
    
    def idMatriculaPrograma(self):
        return "%s" % (self.matricula_programa.id)
    
    def nombre_programa(self):
        return self.matricula_programa.nombre_programa()
    
    def codigo_estudiante(self):
        return self.matricula_programa.codigo
    
    def codigo_ciclo(self):
        return self.ciclo.codigo
    
    def cicloActual(self):
        return self.ciclo.cicloActual()
    
    def nombre_estudiante(self):
        return self.matricula_programa.nombre_estudiante()
    
    def materias_inscritas(self):
        tmp_calificacion = Calificacion.objects.filter(matricula_ciclo = self.id)
        return len(tmp_calificacion)
    
    def promedioCiclo(self, matricula_ciclo_id):
        tmp_calificacion = Calificacion.objects.filter(matricula_ciclo = matricula_ciclo_id)
        tmp_promedio_ciclo = 0.0
        
        for tmp_nota in tmp_calificacion:
            if tmp_nota.tipoValoracion() == "1":
                if tmp_nota.nota_definitiva >= tmp_nota.nota_habilitacion:
                    tmp_promedio_ciclo = tmp_promedio_ciclo + tmp_nota.nota_definitiva
                else: 
                    tmp_promedio_ciclo = tmp_promedio_ciclo + tmp_nota.nota_habilitacion
              
        self.promedio_ciclo = round(tmp_promedio_ciclo/len(tmp_calificacion), 2)
        MatriculaCiclo.save(self)
        self.matricula_programa.calculaPromedioAcumulado(self.matricula_programa.id)
    
    def puesto(self):
        # TODO: Calcular el puesto que ocupa el estudiante en ese ciclo
        return ""
    
    class Meta:
        unique_together = ("matricula_programa", "ciclo")
        verbose_name = 'Matrícula ciclo'
        verbose_name_plural = 'Matrícula ciclos'


class MatriculaCicloForm(ModelForm):
    class Meta:
        model = MatriculaCiclo
                
    
class Curso(models.Model):
    materia = models.ForeignKey(Materia)
    ciclo = models.ForeignKey(Ciclo)
    profesor = models.ForeignKey(Profesor)
    grupo = models.CharField(help_text='Número del grupo 1, 2, 3, ...', max_length=2, validators=[validar_numerico])
    esperados = models.SmallIntegerField(help_text='Número esperado de estudiantes.', blank=True, null=True, validators=[MinValueValidator(0)])
    
    def __unicode__(self):
#        return "%s" %(self.materia)
        return normalizar_cadena(self.materia.nombre)
    
    def promedio(self):
        if self.materia.tipo_valoracion == "1":
            calificaciones = Calificacion.objects.filter(curso = self.id)
            promedio_curso = 0.0
            
            for tmp_nota in calificaciones:
                if tmp_nota.nota_definitiva >= tmp_nota.nota_habilitacion:
                    promedio_curso = promedio_curso + tmp_nota.nota_definitiva
                else: 
                    promedio_curso = promedio_curso + tmp_nota.nota_habilitacion
            
            if len(calificaciones)>0:
                promedio = round(promedio_curso/len(calificaciones), 2)
            else:
                promedio = 0
        else:
            promedio = '-'
        return "%s" % (promedio)
        
    def nombre(self):
        return self.materia.nombre
    
    def codigo(self):
        return "%s-%s" % (self.materia.codigo, self.grupo)
    
    def idMateria(self):
        return "%s" % (self.materia.id)
    
    def codigoMateria(self):
        return "%s" % (self.materia.codigo)
    
    def idPrograma(self):
        return self.materia.idPrograma()
    
    def codigoPrograma(self):
        return "%s" % (self.materia.codigoPrograma())
    
    def nombre_programa(self):
        return "%s" % (self.materia.nombrePrograma())
        
    def notaMin(self):
        return self.materia.notaMin()
    
    def notaMax(self):
        return self.materia.notaMax()
    
    def horarios(self):
        return HorarioCurso.objects.filter(curso=self)
    
    def sesiones(self):
        return len(HorarioCurso.objects.filter(curso=self))
    
    def inscritos(self):
        return len(Calificacion.objects.filter(curso=self))
    
    def tipoValoracion(self):
        return self.materia.tipo_valoracion
    
    class Meta:
        unique_together = ("materia", "ciclo", "profesor", "grupo")
        ordering = ('materia__programa__nombre', 'ciclo', 'materia__nombre')
        
        
class Amonestacion(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    curso = models.ForeignKey(Curso)
    fecha = models.DateField()
    motivo = models.TextField(max_length=200, blank=True, help_text='Motivo por el cual se hace el llamado de atención.')
    
    class Meta:
        verbose_name_plural = 'amonestaciones'

class Calificacion(models.Model):
    curso = models.ForeignKey(Curso)
    matricula_ciclo = models.ForeignKey(MatriculaCiclo)
    nota_definitiva = models.FloatField(blank=True, null=True, default=0)
    nota_habilitacion = models.FloatField(verbose_name='Nota habilitación', blank=True, null=True, default=0)
    fallas = models.IntegerField(help_text="Número de total de fallas en el ciclo.", blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    perdio_fallas = models.BooleanField(verbose_name='Perdió por fallas')
    tipo_aprobacion = models.ForeignKey(TipoAprobacion, default=1)
    
    class Meta:
        unique_together = ("curso", "matricula_ciclo")
        verbose_name_plural = 'Calificaciones'
        ordering = ('matricula_ciclo__ciclo__codigo', 'curso__materia__nombre')
    
    def codigo_estudiante(self): # Metodo para mejorar la lectura en la GUI
        return "%s" % (self.matricula_ciclo)
    
    def nombre_estudiante(self):
        return "%s" % (self.matricula_ciclo.nombre_estudiante())
    
    def codigo_ciclo(self):
        return self.matricula_ciclo.codigo_ciclo()
    
    def codigo_curso(self):
        return self.curso.codigo()
    
    def cicloActual(self):
        return self.matricula_ciclo.cicloActual()
        
    def __unicode__(self):
        return "%s" % (self.curso)
    
    def idMateria(self):
        return "%s" % (self.curso.idMateria())
    
    def codigoMateria(self):
        return "%s" % (self.curso.codigoMateria())
    
    def nombre_materia(self):
        return u"%s" % (self.curso.nombre())
    
    def idMatriculaPrograma(self):
        return "%s" % (self.matricula_ciclo.idMatriculaPrograma())
    
    def idPrograma(self):
        return "%s" % (self.curso.idPrograma())
    
    def codigoPrograma(self):
        return "%s" % (self.curso.codigoPrograma())
    
    def nombre_programa(self):
        return "%s" % (self.curso.nombre_programa())
    
    def horarios(self):
        return self.curso.horarios()
    
    def tipoValoracion(self):
        return self.curso.tipoValoracion()
    
    def abreviatura_aprobacion(self):
        return "%s" % (self.tipo_aprobacion.get_codigo())
    
    def calculaDefinitiva(self, calificacion_id):
        tmp_notas = NotaCorte.objects.filter(calificacion = calificacion_id)
        tmp_calificacion = 0.0
        tmp_fallas = 0
#        Valoración numérica. Suma las notas de los cortes por el porcentaje de corte equivalente. Caso valoración numérica.
        if self.curso.materia.tipo_valoracion=="1":
            for tmp_nota in tmp_notas:
                tmp_corte = Corte.objects.get(id = tmp_nota.corte_id)
                tmp_calificacion = tmp_calificacion + (tmp_nota.nota * (tmp_corte.porcentaje * 0.01))
                tmp_fallas = tmp_fallas + tmp_nota.fallas
                  
            self.nota_definitiva = round(tmp_calificacion, 2)
            self.fallas = tmp_fallas
            Calificacion.save(self)
            
#       Valoración por horas. Suma las horas de los cortes,como el caso de bienestar institucional.
        if self.curso.materia.tipo_valoracion=="3":
            for tmp_nota in tmp_notas:
                tmp_corte = Corte.objects.get(id = tmp_nota.corte_id)
                tmp_calificacion = tmp_calificacion + tmp_nota.nota
                tmp_fallas = tmp_fallas + tmp_nota.fallas
                  
            self.nota_definitiva = tmp_calificacion
            self.fallas = tmp_fallas
            Calificacion.save(self)
        self.matricula_ciclo.promedioCiclo(self.matricula_ciclo.id)
    
    def save(self, *args, **kwargs):
        super(Calificacion, self).save(*args, **kwargs)  
        horas = 0
        matCiclos = MatriculaCiclo.objects.filter(matricula_programa = self.idMatriculaPrograma())
        for matCiclo in matCiclos:
            calificaciones = Calificacion.objects.filter(matricula_ciclo = matCiclo.id)
            for calificacion in calificaciones:
                if calificacion.tipoValoracion() == "3" and calificacion.id != self.id:
                    horas = horas + calificacion.nota_definitiva     
        matricula = MatriculaPrograma.objects.get(id = self.idMatriculaPrograma())
        cal = Calificacion.objects.get(id = self.id)
        matricula.horas_bienestar = horas + cal.nota_definitiva
        super(MatriculaPrograma, matricula).save(*args, **kwargs)  
        
    
class Corte(models.Model):
    ciclo = models.ForeignKey(Ciclo)
    sufijo = models.CharField(max_length=2, help_text="Ingrese el identificador del corte en el ciclo. Debe ser numérico.", validators=[validar_numerico])
    porcentaje = models.IntegerField(help_text="Ingrese un número entre 1 y 100.", validators=[validar_porcentaje])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __unicode__(self):
        return self.ciclo.codigo + "-" + self.sufijo
    
    def corte_actual(self):
        hoy = datetime.date.today() 
        return self.fecha_inicio <= hoy <= self.fecha_fin
    
    def codigo_corte(self):
        return self.ciclo.codigo + "-" + self.sufijo
        
    class Meta:
        unique_together = ("ciclo", "sufijo")
        
class NotaCorte(models.Model):
    calificacion = models.ForeignKey(Calificacion)
    corte = models.ForeignKey(Corte)
#    TODO: corregir validar_nota, las notas ya no son estáticas
    nota = models.FloatField(blank=True, null=True)
    fallas = models.IntegerField(help_text="Número de fallas durante el corte.", blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    comportamiento = models.ForeignKey(TipoComportamiento, blank=True, null=True, default=1)
     
    def save(self, *args, **kwargs):
        super(NotaCorte, self).save(*args, **kwargs)
        self.calificacion.calculaDefinitiva(self.calificacion.id)
    
    def delete(self, *args, **kwargs):
        super(NotaCorte, self).delete(*args, **kwargs)
        self.calificacion.calculaDefinitiva(self.calificacion.id)
    
    class Meta:
        unique_together = ("calificacion", "corte")
 
class HorarioCurso(models.Model):
    curso = models.ForeignKey(Curso)
    dia = models.ForeignKey(Dia, blank=True, null=True, default=1) 
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    salon = models.ForeignKey(Salon, verbose_name='Salón')
    
    def __unicode__(self):
        return "%s %s - %s %s" % (self.dia.nombre, self.hora_inicio.strftime("%H:%M"), self.hora_fin.strftime("%H:%M"), self.salon)
    
    class Meta:
        unique_together = ("dia", "hora_inicio","hora_fin", "salon")


class Institucion(models.Model):
    nombre = models.CharField(max_length=200)
    nit = models.CharField(max_length=20)
    resolucion = models.TextField( verbose_name='Resolución', max_length=200, blank=True)
    direccion = models.CharField( verbose_name='Dirección', max_length=200, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)
    logo = models.ImageField(storage=CustomStorage(), upload_to='imagenes/original/', blank=True)
    control_acudiente = models.BooleanField(help_text="Activado, impide que estudiantes menores de edad cambien la contraseña.")
    class Meta:
        verbose_name_plural = 'Institución'
    
    def __unicode__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        
#        OPCIÓN PARA CARGAR FOTO EN TAMAÑO ORIGINAL, MINI Y THUMNAIL
        existe_logo = False
        if self.logo.name != "":
            tmp_logo = self.nit + "c.jpg"
            self.logo.name = "imagenes/original/" + tmp_logo
            existe_logo = True        
         
        super(Institucion, self).save(*args, **kwargs)
        
        if existe_logo == True:
            logo_org = settings.MEDIA_ROOT + "imagenes/original/" + tmp_logo
            logo_min = settings.MEDIA_ROOT + "imagenes/mini/" + tmp_logo
            logo_thu = settings.MEDIA_ROOT + "imagenes/thumbnail/" + tmp_logo
            
            scale(logo_org, THUMB_WIDTH, THUMB_HEIGHT, logo_thu)
            scale(logo_org, MINI_WIDTH, MINI_HEIGHT, logo_min)
           

class ConfiguracionInscripcion(models.Model):
    ciclo = models.ForeignKey(Ciclo)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    class Meta:
        verbose_name_plural = 'Configuración inscripciones'


class Funcionario(models.Model):
    institucion = models.ForeignKey(Institucion)
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True, default=1) 
    documento = models.CharField(max_length=12, unique = True, validators=[validar_numerico])
    lugar_expedicion = models.CharField(verbose_name='Lugar expedición', max_length=200, blank=True)
    tipo_funcionario = models.ForeignKey(TipoFuncionario, blank=True, null=True, default=1) 
    
    def __unicode__(self):
        return self.tipo_funcionario.nombre