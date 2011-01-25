# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


NOTA_MIN = 0.0
NOTA_MAX = 5.0
NOTA_APR = 3.5

def crear_usuario(nombre1, nombre2, apellido1, apellido2):
    # TODO: Verificar si el nombre de usuario es unico
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
                num_usuario = total_usuarios
            else:
                repetido = False
                usuario = tmp_usuario
                
        return usuario

def normalizar_usuario(cadena):
    # Remueve caracteres especiales y espacios de los nombres de usuario.
    cadena = cadena.lower()
    cadena = cadena.replace("á", "a")
    cadena = cadena.replace("é", "e")
    cadena = cadena.replace("í", "i")
    cadena = cadena.replace("ó", "o")
    cadena = cadena.replace("ú", "u")
    cadena = cadena.replace("ü", "u")
    cadena = cadena.replace("ñ", "n")
    cadena = cadena.replace(" ", "_")
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


class TipoPrograma(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre


def validar_nota(nota):
        if nota < NOTA_MIN or nota > NOTA_MAX:
            raise ValidationError("%s no es una nota válida" % nota)
        
def validar_porcentaje(porcentaje):
        if porcentaje < 1 or porcentaje > 100:
            raise ValidationError("%s no es una porcentaje válido" % porcentaje)

def validar_digito(digito):
    if not digito.isdigit():
        raise ValidationError("%s no es dígito válido" % digito)

def validar_numerico(cifra):
    for c in cifra:
        if not c.isdigit():
            raise ValidationError('%s no es valor numérico válido' % cifra)

class Ciclo(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=8, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    

    def __unicode__(self):
        return self.codigo
    
    def cortes(self):
        return len(Corte.objects.filter(ciclo=self))
        
        
        
class Profesor(models.Model):
    # Informacion personal
    nombre1 = models.CharField(max_length=50, verbose_name='Primer nombre')
    nombre2= models.CharField(max_length=50, verbose_name='Segundo nombre', blank=True)
    apellido1 = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido2 = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True)
    genero = models.ForeignKey(Genero, blank=True, null=True, default=1) 
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True, default=1) 
    documento = models.CharField(max_length=12, unique = True, validators=[validar_numerico])
    lugar_expedicion = models.CharField(verbose_name='Lugar expedición', max_length=200, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(blank=True, max_length=200)
    foto = models.ImageField(upload_to='imagenes/original/', blank=True)
    
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
        if self.foto.name != "":
            self.foto.name = self.documento + "c.jpg"
        
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
    
    def usuario(self):
        user = User.objects.get(id=self.id_usuario)
        return user
        
    def __unicode__(self):
        return "%s %s" % (self.nombre1, self.apellido1) 
    
    class Meta:
        verbose_name_plural = 'profesores'


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
    actitudes = models.TextField(max_length=200, help_text="Actitudes requeridas para los aspirantes.", blank=True)
    perfil_profesional = models.TextField(max_length=200, help_text="Perfil profesional del egresado.", blank=True)
    funciones = models.TextField(max_length=200,help_text="Funciones en las que se puede desempeñar el egresado.", blank=True)
    
    def competencias(self):
        return len(Competencia.objects.filter(programa=self))
    
    def __unicode__(self):
        return "%s - %s" % (self.codigo, self.nombre)


class Estudiante(models.Model):
    
    # Identificacion
    nombre1 = models.CharField(max_length=50, verbose_name='Primer nombre')
    nombre2= models.CharField(max_length=50, verbose_name='Segundo nombre', blank=True)
    apellido1 = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido2 = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True)
    genero = models.ForeignKey(Genero, blank=True, null=True, default=1) 
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True, default=1) 
    documento = models.CharField(max_length=12, unique = True, validators=[validar_numerico])
    lugar_expedicion = models.CharField(max_length=200, verbose_name='Lugar expedición', blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=200, blank=True)
    
    # Requisitos
    fotocopia_documento = models.ImageField(upload_to='imagenes/original/', blank=True)
    fotocopia_diploma = models.ImageField(upload_to='imagenes/original/', blank=True)
    foto = models.ImageField(upload_to='imagenes/original/', blank=True)
    
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
    
#       Sobreescribir la función guardar para crear usuario
#       Guardar información de acceso a la tabla de usuarios de DJANGO
#       Grupo 4 corresponde en la base de datos con un perfil estudiante

    def save(self, *args, **kwargs):
        if self.fotocopia_documento.name != "":
            self.fotocopia_documento.name = self.documento + "a.jpg"
        if self.fotocopia_diploma.name != "":
            self.fotocopia_diploma.name = self.documento + "b.jpg"
        if self.foto.name != "":
            self.foto.name = self.documento + "c.jpg"
        
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
    
    def usuario(self):
        user = User.objects.get(id=self.id_usuario)
        return user
    
    def __unicode__(self):
        return self.documento


class OtrosEstudiosEstudiante(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    tipo_estudio = models.ForeignKey(TipoEstudio, blank=True, null=True, default=1) 
    institucion = models.CharField( verbose_name='Institución', max_length=200,  blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, blank=True)
    fecha_graduacion = models.DateField(verbose_name='Fecha graduación', blank=True, null=True)


class Referencia(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    tipo_referencia = models.ForeignKey(TipoReferencia, blank=True, null=True, default=1) 
    nombre = models.CharField(max_length=20, blank=True)
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
    promedio_acumulado = models.FloatField(blank=True, null=True, validators=[validar_nota])
    
    def nombre_estudiante(self):
        return self.estudiante.nombre1 + ' ' + self.estudiante.apellido1
    
    def nombre_programa(self):
        return self.programa.nombre
     
#    Asignar automáticamente código de inscripción a estudiante
#    Se usó sentencia mysql y se requiere modificar settings en mysql
    def save(self, *args, **kwargs):
        tmp_codigo = "%s%s%s" %(self.programa.codigo, self.fecha_inscripcion.strftime("%y"), '0001')
        if len(MatriculaPrograma.objects.filter(codigo=tmp_codigo)) == 0:
            self.codigo = tmp_codigo
        else:
            tmp_codigo = tmp_codigo[0:4]
            for c in MatriculaPrograma.objects.raw('SELECT id, lpad(cast(right(codigo, 4) as signed)+1, 4, 0) AS codigo FROM academico_MatriculaPrograma where left(codigo, 4) = %s limit 0, 1', [tmp_codigo]):
                self.codigo = "%s%s" %(tmp_codigo, c.codigo)
            
        super(MatriculaPrograma, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.codigo
    
    class Meta:
        unique_together = ("estudiante", "programa")
        verbose_name = 'Matrícula programa'
        verbose_name_plural = 'Matrícula programas' 

class Competencia(models.Model):
    programa = models.ForeignKey(Programa)
    codigo = models.CharField(max_length=10)
    sufijo = models.CharField(max_length=3, help_text='El sufijo se añade al código del programa y forma el código')
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    creditos = models.IntegerField(help_text='Número de créditos de la competencia.', blank=True, null=True)
    periodo = models.SmallIntegerField(help_text='Nivel en el cual se debe ver esta competencia.', blank=True, null=True)
    intensidad = models.SmallIntegerField(help_text='Número de horas requeridas para dictar la compentencia.', blank=True, null=True, validators=[MinValueValidator(0)])
    
    def save(self, *args, **kwargs):
        self.codigo = "%s%s" % (self.programa.codigo, self.sufijo)
        super(Competencia, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.codigo
    
    def grupos(self):
        return len(Curso.objects.filter(competencia=self))
    
    def nombrePrograma(self):
        return "%s" % (self.programa.nombre)
  
  
class MatriculaCiclo(models.Model):
    fecha_inscripcion = models.DateField()
    matricula_programa = models.ForeignKey(MatriculaPrograma)
    ciclo = models.ForeignKey(Ciclo)
    observaciones = models.TextField(max_length=200, blank=True)
    
    def __unicode__(self):
        return self.matricula_programa.codigo
  
    def nombre_programa(self):
        return self.matricula_programa.nombre_programa()
    
    def codigo_estudiante(self):
        return self.matricula_programa.codigo
    
    def nombre_estudiante(self):
        return self.matricula_programa.nombre_estudiante()
    
    def promedio_periodo(self):
        # TODO: Calcular el promedio de las materias cursadas en ese ciclo
        return ""
  
    def puesto(self):
        # TODO: Calcular el puesto que ocupa el estudiante en ese ciclo
        return ""
    
    class Meta:
        unique_together = ("matricula_programa", "ciclo")
        verbose_name = 'Matrícula ciclo'
        verbose_name_plural = 'Matrícula ciclos'


    
    
class Curso(models.Model):
    competencia = models.ForeignKey(Competencia)
    ciclo = models.ForeignKey(Ciclo)
    profesor = models.ForeignKey(Profesor)
    grupo = models.CharField(help_text='Número del grupo 1, 2, 3, ...', max_length=2, validators=[validar_numerico])
    estudiantes_esperados = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    estudiantes_inscritos = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    
    def __unicode__(self):
        return self.codigo()
    
    def nombre(self):
        return self.competencia.nombre
    
    def codigo(self):
        return "%s-%s" % (self.competencia.codigo, self.grupo)
    
    def idCompetencia(self):
        return "%s" % (self.competencia.id)
    
    def codigoCompetencia(self):
        return "%s" % (self.competencia.codigo)
    
    def nombrePrograma(self):
        return "%s" % (self.competencia.nombrePrograma())
    
    def horarios(self):
        return HorarioCurso.objects.filter(curso=self)
    
    def sesiones(self):
        return len(HorarioCurso.objects.filter(curso=self))
    
    class Meta:
        unique_together = ("competencia", "ciclo", "profesor", "grupo")
        
        
        
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
    nota_definitiva = models.FloatField(blank=True, null=True, validators=[validar_nota])
    nota_habilitacion = models.FloatField(verbose_name='Nota habilitación', blank=True, null=True, validators=[validar_nota])
    perdio_fallas = models.BooleanField(verbose_name='Perdió por fallas')

    class Meta:
        unique_together = ("curso", "matricula_ciclo")
        verbose_name_plural = 'Calificaciones'
    
    def codigo_estudiante(self): # Metodo para mejorar la lectura en la GUI
        return "%s" % (self.matricula_ciclo)
        
    def __unicode__(self):
        return "%s" % (self.curso)
    
    def idCompetencia(self):
        return "%s" % (self.curso.idCompetencia())
    
    def codigoCompetencia(self):
        return "%s" % (self.curso.codigoCompetencia())
    
    def nombreCompetencia(self):
        return "%s" % (self.curso.nombre())
    
    def nombrePrograma(self):
        return "%s" % (self.curso.nombrePrograma())
    
    def horarios(self):
        return self.curso.horarios()

class Corte(models.Model):
    ciclo = models.ForeignKey(Ciclo)
    codigo = models.CharField(verbose_name="Código", max_length=12, unique=True)
    porcentaje = models.IntegerField(help_text="Ingrese un número entre 1 y 100.", validators=[validar_porcentaje])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
  
    def __unicode__(self):
        return self.codigo


class NotaCorte(models.Model):
    calificacion = models.ForeignKey(Calificacion)
    corte = models.ForeignKey(Corte)
    nota = models.FloatField(blank=True, null=True, validators=[validar_nota])
    fallas = models.IntegerField(help_text="Número de fallas durante el corte.", blank=True, null=True, validators=[MinValueValidator(0)])
    comportamiento = models.ForeignKey(TipoComportamiento, blank=True, null=True, default=1)
     
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


class SesionCurso(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=12)
    curso = models.ForeignKey(Curso)
    fecha = models.DateField(blank=True, null=True)
  
    def __unicode__(self):
        return self.codigo

