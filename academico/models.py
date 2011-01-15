# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


NOTA_MIN = 0.0
NOTA_MAX = 5.0
NOTA_APR = 3.5

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

class Ciclo(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=8)
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
    documento = models.CharField(max_length=12, unique = True)
    lugar_expedicion = models.CharField(verbose_name='Lugar expedición', max_length=200, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(blank=True, max_length=200)
    foto = models.FileField(upload_to='/', blank=True)
    
    # Informacion de contacto
    direccion = models.CharField(verbose_name='Dirección', max_length=200, blank=True)
    lugar_residencia = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=20, blank=True)
    movil = models.CharField(verbose_name='Móvil', max_length=20, blank=True)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)
 
#    Sobreescribir la función guardar para crear usuario
#    Guardar información de acceso a la tabla de usuarios de DJANGO
#    Grupo 3 corresponde en la base de datos con un perfil profesor

    def save(self, *args, **kwargs):
        try:
                user = User.objects.get(username=self.documento)
        except User.DoesNotExist:
                user = User.objects.create_user(self.documento, self.email, self.documento)
                user.groups.add(3);
                user.save()
                
        user.is_staff = False
        user.first_name = self.nombre1
        user.last_name = self.apellido1
        user.email = self.email
        user.save()
        super(Profesor, self).save(*args, **kwargs)  
        
    def __unicode__(self):
        return "%s %s" % (self.nombre1, self.apellido1) 
    
    class Meta:
        verbose_name_plural = 'profesores'


class ExperienciaLaboralProfesor(models.Model):
    profesor = models.ForeignKey(Profesor)
    cargo = models.CharField(max_length=200, blank=True)
    empresa = models.CharField(max_length=200, blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    actualmente = models.BooleanField()
  
    class Meta:
        verbose_name_plural = 'experiencia laboral profesores'


class OtrosEstudiosProfesor(models.Model):
    profesor = models.ForeignKey(Profesor)
    tipo_estudio = models.ForeignKey(TipoEstudio, blank=True, null=True, default=1)
    institucion = models.CharField(verbose_name='Institución', max_length=200, blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, blank=True)
    fecha_graduacion = models.DateField(verbose_name='Fecha graduación', blank=True, null=True)
    class Meta:
        verbose_name_plural = 'otros estudios profesores'


class Salon(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=12)
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
    codigo = models.CharField(verbose_name='Código', max_length=2)
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
    documento = models.CharField(max_length=12, unique = True)
    lugar_expedicion = models.CharField(max_length=200, verbose_name='Lugar expedición', blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=200, blank=True)
    
    # Requisitos
    fotocopia_documento = models.FileField(upload_to='/', blank=True)
    fotocopia_diploma = models.FileField(upload_to='/', blank=True)
    foto = models.FileField(upload_to='/', blank=True)
    
    # Informacion de contacto
    direccion = models.CharField( verbose_name='Dirección', max_length=200, blank=True)
    lugar_residencia = models.CharField(max_length=200, blank=True)
    estrato = models.ForeignKey(Estrato, blank=True, null=True, default=4)
    telefono = models.CharField(verbose_name='Teléfono', max_length=20, blank=True)
    movil = models.CharField(verbose_name='Móvil', max_length=20, blank=True)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)
    
    # Informacion de acceso
#    usuario = models.CharField(max_length=12, unique=True)
#    contrasena = models.CharField(verbose_name='Contraseña', max_length=50, blank=True)
    
    # Informacion adicional
    sisben = models.ForeignKey(Sisben, blank=True, default=1, null=True)
    discapacidad = models.ForeignKey(Discapacidad, blank=True, default=1, null=True)
    etnia = models.ForeignKey(Etnia, default=1, blank=True, null=True)
    
#       Sobreescribir la función guardar para crear usuario
#       Guardar información de acceso a la tabla de usuarios de DJANGO
#       Grupo 4 corresponde en la base de datos con un perfil estudiante

    def save(self, *args, **kwargs):
        try:
                user = User.objects.get(username=self.documento)
        except User.DoesNotExist:
                user = User.objects.create_user(self.documento, self.email, self.documento)
                user.groups.add(4);
                user.save()
                
        user.is_staff = False
        user.first_name = self.nombre1
        user.last_name = self.apellido1
        user.email = self.email
        user.save()
        super(Estudiante, self).save(*args, **kwargs)  
    
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


class InscripcionEstudiantePrograma(models.Model):
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
        if len(InscripcionEstudiantePrograma.objects.filter(codigo=tmp_codigo)) == 0:
            self.codigo = tmp_codigo
        else:
            tmp_codigo = tmp_codigo[0:4]
            for c in InscripcionEstudiante.objects.raw('SELECT id, lpad(cast(right(codigo, 4) as signed)+1, 4, 0) AS codigo FROM academico_InscripcionEstudiante where left(codigo, 4) = %s limit 0, 1', [tmp_codigo]):
                self.codigo = "%s%s" %(tmp_codigo, c.codigo)
            
        super(InscripcionEstudiantePrograma, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.codigo
    
    class Meta:
        verbose_name_plural = 'Inscripción estudiante a Programa' 

class Competencia(models.Model):
    programa = models.ForeignKey(Programa)
    codigo = models.CharField(verbose_name='Código',  max_length=12)
    nombre = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)

    periodo = models.IntegerField(help_text='Nivel en el cual se debe ver esta competencia.', blank=True, null=True)
    intensidad = models.SmallIntegerField(help_text='Número de horas requeridas para dictar la compentencia.', blank=True, null=True, validators=[MinValueValidator(0)])
    
    def __unicode__(self):
        return self.codigo
  
  
class InscripcionProgramaCiclo(models.Model):
#    fecha_vencimiento = models.DateField(blank=True, null=True)
#    promedio_periodo = models.FloatField(blank=True, null=True, validators=[validar_nota])
    fecha_inscripcion = models.DateField()
    inscripcion_estudiante_programa = models.ForeignKey(InscripcionEstudiantePrograma)
    ciclo = models.ForeignKey(Ciclo)
    puesto = models.SmallIntegerField(help_text='Puesto ocupado durante el periodo academico.', blank=True, null=True)
    observaciones = models.TextField(max_length=200, blank=True)
    
    def nombre_programa(self):
        return self.inscripcion_estudiante_programa.nombre_programa()
    
    def nombre_estudiante(self):
        return self.inscripcion_estudiante_programa.nombre_estudiante()
    def promedioPeriodo(self):
        return ""
  

class Amonestacion(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    profesor = models.ForeignKey(Profesor)
    competencia = models.ForeignKey(Competencia)
    fecha = models.DateField()
    motivo = models.TextField(max_length=200, blank=True, help_text='Motivo por el cual se hace el llamado de atención.')
    
    class Meta:
        verbose_name_plural = 'amonestaciones'
    
    
class Curso(models.Model):
    competencia = models.ForeignKey(Competencia)
    codigo = models.CharField(verbose_name='Código', max_length=12)
    ciclo = models.ForeignKey(Ciclo)
    profesor = models.ForeignKey(Profesor)
    grupo = models.CharField(help_text='Número del grupo 1, 2, 3, ...', max_length=2, validators=[validar_digito])
    estudiantes_esperados = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    estudiantes_inscritos = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    
    def __unicode__(self):
        return self.codigo
    
    def competencia_nombre(self):
        return self.competencia.nombre
    
    def save(self, *args, **kwargs):
        self.codigo = "%s-%s" % (self.competencia.codigo, self.grupo)
        super(Curso, self).save(*args, **kwargs)
        
        
class Calificacion(models.Model):
    curso = models.ForeignKey(Curso)
    inscripcion_programa_ciclo = models.ForeignKey(InscripcionProgramaCiclo)
    nota_definitiva = models.FloatField(blank=True, null=True, validators=[validar_nota])
    nota_habilitacion = models.FloatField(verbose_name='Nota habilitación', blank=True, null=True, validators=[validar_nota])
    perdio_fallas = models.BooleanField(verbose_name='Perdió por fallas')

    class Meta:
        verbose_name_plural = 'Calificaciones'

class Corte(models.Model):
    ciclo = models.ForeignKey(Ciclo)
    codigo = models.CharField(verbose_name="Código", max_length=12)
    porcentaje = models.IntegerField(help_text="Ingrese un número entre 1 y 100.", blank=True, validators=[validar_porcentaje])
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
  
    def __unicode__(self):
        return self.codigo


class NotaCorte(models.Model):
    calificacion = models.ForeignKey(Calificacion)
    corte = models.ForeignKey(Corte)
    nota = models.FloatField(blank=True, null=True, validators=[validar_nota])
    fallas = models.IntegerField(help_text="Número de fallas durante el corte.", blank=True, null=True, validators=[MinValueValidator(0)])
    comportamiento = models.ForeignKey(TipoComportamiento, blank=True, null=True, default=1)
     

  
class HorarioCurso(models.Model):
    curso = models.ForeignKey(Curso)
    dia = models.ForeignKey(Dia, blank=True, null=True, default=1) 
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    salon = models.ForeignKey(Salon, verbose_name='Salón')


class SesionCurso(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=12)
    curso = models.ForeignKey(Curso)
    fecha = models.DateField(blank=True, null=True)
  
    def __unicode__(self):
        return self.codigo


class Asistencia(models.Model):
    sesion_curso = models.ForeignKey(SesionCurso)
    inscripcion_estudiante_programa = models.ForeignKey(InscripcionEstudiantePrograma)
    asistio = models.BooleanField(verbose_name='Asistió', default=True)
    observaciones = models.TextField(max_length=200, blank=True)