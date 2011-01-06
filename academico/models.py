# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

NOTA_MIN = 0.0
NOTA_MAX = 5.0
NOTA_APR = 3.5

SISBEN = (
    ('1', '1'),  
    ('2', '2'), 
    ('3', '3'), 
    ('4', '4'), 
    ('5', '5'), 
    ('6', '6'), 
    ('9','No aplica'),
)

ETNIA = (
    ('00', 'No Aplica'), 
    ('01', 'Achagua'), 
    ('02', 'Amorúa'), 
    ('03', 'Andoque o Andoke'), 
    ('04', 'Arhuaco (IJKA)'), 
    ('05', 'Awa (CUAIKER)'), 
    ('06', 'Barea'), 
    ('07', 'Barazana'), 
    ('08', 'Barí (Motilón)'), 
    ('09', 'Betoye'), 
    ('10', 'Bora'), 
    ('11', 'Cabiyari o Kawiyarí'), 
    ('12', 'Carapana'),
    ('13', 'Carijona o Karijona'),
    ('14', 'Chimila (ETTE E´ NEKA)'), 
    ('15', 'Chiricoa'), 
    ('16', 'Cocama'),
    ('17', 'Coconuco'),
    ('18', 'Cofán o Kofán'), 
    ('19', 'Pijaos'),
    ('20', 'Cubeo o Kubeo'),
    ('21', 'Cuiba o Kuiba'),
    ('22', 'Curripaco o Kurripako'), 
    ('23', 'Desano'),
    ('24', 'Dujos'),
    ('26', 'Embera Catio o Embera Katío'), 
    ('27', 'Embera Chami'),
    ('28', 'Eperara Siapidara'), 
    ('29', 'Guambiano'), 
    ('30', 'Guanaca'),
    ('31', 'Guayabero'), 
    ('33', 'Hitnú'),
    ('34', 'Inga'),
    ('35', 'Kamsa o Kamëntsá'), 
    ('36', 'Kogui'),
    ('37', 'Koreguaje o Coreguaje'), 
    ('38', 'Letuama'),
    ('39', 'Macaguaje o Makaguaje'), 
    ('40', 'Nukak (Makú)'),
    ('41', 'Macuna o Makuna (Sara)'), 
    ('42', 'Masiguare'), 
    ('43', 'Matapí'),
    ('44', 'Miraña'),
    ('45', 'Muinane'),
    ('46', 'Muisca'),
    ('47', 'Nonuya'),
    ('48', 'Ocaina'),
    ('49', 'Nasa (Paéz)'), 
    ('50', 'Pastos'),
    ('51', 'Piapoco (Dzase)'), 
    ('52', 'Piaroa'),
    ('53', 'Piratapuyo'), 
    ('54', 'Pisamira'),
    ('55', 'Puinave'),
    ('56', 'Sáliba'),
    ('57', 'Sikuani'), 
    ('58', 'Siona'),
    ('59', 'Siriano'),
    ('60 ', 'iripu o Tsiripu (Mariposo)'), 
    ('61', 'Taiwano (Tajuano)'), 
    ('62', 'TanimuKa'),
    ('63', 'Tariano'),
    ('64', 'Tatuyo'),
    ('65', 'Tikuna'), 
    ('66', 'Totoró'),
    ('67', 'Tucano (Desea) o Tukano'), 
    ('68', 'Tule (Kuna)'),
    ('69', 'Tuyuka (Dojkapuara)'), 
    ('70', 'U´wa (Tunebo)'), 
    ('71', 'Wanano'),
    ('72', 'Wayuu'),
    ('73', 'Witoto'),
    ('74', 'Wiwa (Arzario)'),
    ('75', 'Waunan (Wuanana)'), 
    ('76', 'Yagua'),
    ('77', 'Yanacona'), 
    ('78', 'Yauna'), 
    ('79', 'Yukuna'),
    ('80', 'Yuko (Yukpa)'), 
    ('81', 'Yurí (Carabayo)'), 
    ('82', 'Yuruti'), 
    ('83', 'Zenú'),
    ('84', 'Quillacingas'),
    ('200', 'Negritudes'), 
    ('400', 'Rom'),
)

TIPO_COMPORTAMIENTO = (
    ('E', 'Excelente'),
    ('B', 'Bueno'),
    ('A', 'Aceptable'),
    ('I', 'Insuficiente'),
    ('N', 'No aplica'),
)

ESTRATO = (
    ('0', 'Estrato 0'),
    ('1', 'Estrato 1'),
    ('2', 'Estrato 2'),
    ('3', 'Estrato 3'),
    ('4', 'Estrato 4'),
    ('5', 'Estrato 5'),
    ('6', 'Estrato 6'),
)

ESTADO_INSCRIPCION = (
    ('A', 'Activo'),
    ('E', 'Egresado'),
    ('X', 'Expulsado'),
    ('R', 'Retirado'),
    ('D', 'Suspendido disciplina'),
)

TIPO_DOCUMENTO = (
    ('1', 'Cédula de Ciudadanía'), 
    ('2', 'Tarjeta de Identidad'), 
    ('3', 'Cédula de Extranjería ó Identificación de Extranjería'), 
    ('5', 'Registro Civil de Nacimiento'), 
    ('6', 'Número de Identificación Personal (NIP)'), 
    ('7', 'Número Único de Identificación Personal (NUIP)'), 
    ('8', 'Número de Identificación establecido por la Secretaría de  Educación'),   
    ('9', 'Certificado Cabildo'),
)

GENERO = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)

TIPO_REFERENCIA = (
    ('F', 'Familiar'),
    ('P', 'Personal'),
    ('C', 'Comercial'),
    ('A', 'Académica'),
    ('L', 'Laboral'),
)

DISCAPACIDAD = (
    ('1', 'Sordera Profunda'),  
    ('2', 'Hipoacusia o Baja audición'), 
    ('3', 'Baja visión diagnosticada'),
    ('4', 'Ceguera'), 
    ('5', 'Parálisis cerebral'),  
    ('6', 'Lesión neuromuscular'),  
    ('7', 'Autismo'),
    ('8', 'Deficiencia cognitiva (Retardo Mental)'),  
    ('9', 'Síndrome de Down'),
    ('10', 'Múltiple'),                                                                                                                                
    ('99', 'No aplica'),
)

JORNADA = (
    ('1', 'Completa'),
    ('2', 'Mañana'),
    ('3', 'Tarde'),
    ('4', 'Nocturna'),
    ('5', 'Fin de semana'),
)

MODULO = (
    ('H', 'Humanidades'),
    ('C', 'Ciencias básicas'),
    ('T', 'Técnico'),
)

PERIODICIDAD = (
    ('C', 'Cuatrimestral'),
    ('S', 'Semestral'),
    ('A', 'Anual'),
)

DIAS = (
    ('L', 'Lunes'),
    ('M', 'Martes'),
    ('C', 'Miércoles'),
    ('J', 'Jueves'),
    ('V', 'Viernes'),
    ('S', 'Sábado'),
    ('D', 'Domingo'),
)

TIPO_SALON = (
    ('A', 'Aula'),
    ('L', 'Laboratorio'),
    ('U', 'Auditorio'),
    ('I', 'Aire libre'),
    ('M', 'Aula mantenimiento'),
    ('O', 'Otro'),
)

TIPO_ESTUDIO = (
    ('P', 'Primaria'),
    ('S', 'Secundaria'),
    ('T', 'Técnico'),
    ('U', 'Universitario'),
    ('E', 'Especialización'),
    ('M', 'Maestría'),
    ('D', 'Doctorado'),
    ('O', 'Otros estudios'),
)

TIPO_PROGRAMA = (
    ('T',  'Técnico'),
    ('A',  'Auxiliar'),
)


def validar_nota(nota):
        if nota < NOTA_MIN or nota > NOTA_MAX:
            raise ValidationError(u"%s no es una nota válida" % nota)
        
def validar_porcentaje(porcentaje):
        if porcentaje < 1 or porcentaje > 100:
            raise ValidationError(u"%s no es una porcentaje válido" % porcentaje)

        
class Profesor(models.Model):
    # Informacion personal
    nombre1 = models.CharField(max_length=50, verbose_name='Primer nombre')
    nombre2= models.CharField(max_length=50, verbose_name='Segundo nombre', blank=True)
    apellido1 = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido2 = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True)
    genero = models.CharField(verbose_name='Género', max_length=1, choices=GENERO, blank=True) 
    tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO, blank=True) 
    documento = models.CharField(max_length=12, unique = True)
    lugar_expedicion = models.CharField(verbose_name='Lugar expedición', max_length=200, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    lugar_nacimiento = models.CharField(blank=True, max_length=200)
    foto = models.FileField(upload_to='/', blank=True)
    
    # Informacion de contacto
    direccion = models.CharField(verbose_name='Dirección', max_length=200, blank=True)
    lugar_residencia = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=200, blank=True)
    email = models.EmailField(unique = True, blank=True)
    web = models.URLField(blank=True)
    
    # Informacion de acceso
    usuario = models.CharField(max_length=200, unique=True, blank=True)
    contrasena = models.CharField(verbose_name='Contraseña', max_length=200, blank=True)
  
    def __unicode__(self):
        return self.documento
    
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
    tipo_estudio = models.CharField(max_length=1, choices=TIPO_ESTUDIO, blank=True)
    institucion = models.CharField(verbose_name='Institución', max_length=200, blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, blank=True)
    fecha_graduacion = models.DateField(verbose_name='Fecha graduación', blank=True, null=True)
    class Meta:
        verbose_name_plural = 'otros estudios profesores'


class Salon(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=200)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    capacidad = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    tipo_salon = models.CharField(verbose_name='Tipo salón', max_length=1, choices=TIPO_SALON, blank=True)
    
    def __unicode__(self):
        return self.codigo
    
    class Meta:
        verbose_name_plural = 'salones'


class Programa(models.Model):
    # Informacion general
    tipo_programa = models.CharField(max_length=1, choices=TIPO_PROGRAMA, blank=True)
    codigo = models.CharField(verbose_name='Código', max_length=200)
    nombre = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, help_text='Título otorgado al finalizar el programa.', blank=True)
    resolucion = models.CharField(verbose_name='Resolución', max_length=200, help_text="Acto administrativo que valida este programa.", blank=True)
    snies = models.CharField(verbose_name='SNIES', max_length=200, help_text="Código Sistema Nacional de Información de la Educación Superior.", blank=True)
    # Horario
    periodicidad = models.CharField(max_length=1, choices=PERIODICIDAD, blank=True) 
    duracion = models.IntegerField(verbose_name='Duración', blank=True, null=True, validators=[MinValueValidator(0)])
    jornada = models.CharField(max_length=1, choices=JORNADA, blank=True)
    # Informacion adicional
    actitudes = models.TextField(max_length=200, help_text="Actitudes requeridas para los aspirantes.", blank=True)
    perfil_profesional = models.TextField(max_length=200, help_text="Perfil profesional del egresado.", blank=True)
    funciones = models.TextField(max_length=200,help_text="Funciones en las que se puede desempeñar el egresado.", blank=True)
    def __unicode__(self):
        return self.codigo


class Estudiante(models.Model):
    
    # Identificacion
    nombre1 = models.CharField(max_length=50, verbose_name='Primer nombre')
    nombre2= models.CharField(max_length=50, verbose_name='Segundo nombre', blank=True)
    apellido1 = models.CharField(max_length=50, verbose_name='Primer apellido')
    apellido2 = models.CharField(max_length=50, verbose_name='Segundo apellido', blank=True)
    genero = models.CharField(verbose_name='Género', max_length=1, choices=GENERO, blank=True) 
    tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO, blank=True) 
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
    estrato = models.CharField(max_length=1, choices=ESTRATO, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=200, blank=True)
    email = models.EmailField(unique = True, blank=True)
    web = models.URLField(blank=True)
    
    # Informacion de acceso
    usuario = models.CharField(max_length=200, unique = True, blank=True)
    contrasena = models.CharField(verbose_name='Contraseña', max_length=200, blank=True)
    
    # Informacion adicional
    sisben = models.CharField(max_length=1, choices=SISBEN, blank=True, default='9')
    discapacidad = models.CharField(max_length=2, choices=DISCAPACIDAD, blank=True, default='99')
    etnia = models.CharField(max_length=3, choices=ETNIA, blank=True, default='00')
    
    def __unicode__(self):
        return self.documento


class OtrosEstudiosEstudiante(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    tipo_estudio = models.CharField(max_length=1, choices=TIPO_ESTUDIO, blank=True) 
    institucion = models.CharField( verbose_name='Institución', max_length=200,  blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, blank=True)
    fecha_graduacion = models.DateField(verbose_name='Fecha graduación', blank=True, null=True)


class Referencia(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    tipo_referencia = models.CharField( max_length=1, choices=TIPO_REFERENCIA, blank=True) 
    nombre = models.CharField(max_length=200, blank=True)
    tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO, blank=True)
    documento = models.CharField(max_length=200, blank=True)
    direccion = models.CharField( verbose_name='Dirección', max_length=200, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=200,  blank=True)


class InscripcionEstudiante(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
    programa = models.ForeignKey(Programa)
    codigo = models.CharField(verbose_name='Código', max_length=200, unique = True)
    estado = models.CharField(max_length=1, choices=ESTADO_INSCRIPCION, default='A')
    fecha_vencimiento = models.DateField()
    becado = models.BooleanField(help_text='Indica si el estudiante recibe o no beca.')
    promedio_acumulado = models.FloatField(blank=True, null=True, validators=[validar_nota])
    
    def __unicode__(self):
        return self.codigo


class Competencia(models.Model):
    programa = models.ForeignKey(Programa)
    codigo = models.CharField(verbose_name='Código',  max_length=200)
    nombre = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    modulo = models.CharField(verbose_name='Módulo', max_length=1, choices=MODULO, blank=True)
    periodo = models.IntegerField(help_text='Nivel en el cual se debe ver esta competencia.', blank=True, null=True)
    intensidad = models.IntegerField(help_text='Número de horas requeridas para dictar la compentencia.', blank=True, null=True, validators=[MinValueValidator(0)])
    
    def __unicode__(self):
        return self.codigo
  
  
class MatriculaPrograma(models.Model):
    fecha_expedicion = models.DateField()
    inscripcion_estudiante = models.ForeignKey(InscripcionEstudiante)
    programa = models.ForeignKey(Programa)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    promedio_periodo = models.FloatField(blank=True, null=True, validators=[validar_nota])
    puesto = models.IntegerField(help_text='Puesto ocupado durante el periodo academico.', blank=True, null=True)
    observaciones = models.TextField(max_length=200, blank=True)
  

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
    codigo = models.CharField(verbose_name='Código', max_length=200)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    profesor = models.ForeignKey(Profesor)
    grupo = models.IntegerField(help_text='Número del grupo 1, 2, 3, ...', validators=[MinValueValidator(0)])
    estudiantes_esperados = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    estudiantes_inscritos = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    
    def __unicode__(self):
        return self.codigo



class MatriculaCurso(models.Model):
    curso = models.ForeignKey(Curso)
    inscripcion_estudiante = models.ForeignKey(InscripcionEstudiante)
    nota_definitiva = models.FloatField(blank=True, null=True, validators=[validar_nota])
    nota_habilitacion = models.FloatField(verbose_name='Nota habilitación', blank=True, null=True, validators=[validar_nota])
    perdio_fallas = models.BooleanField(verbose_name='Perdió por fallas')




class Corte(models.Model):
    codigo = models.CharField(verbose_name="Código", max_length=200)
    porcentaje = models.IntegerField(help_text="Ingrese un número entre 1 y 100.", blank=True, validators=[validar_porcentaje])
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
  
    def __unicode__(self):
        return self.codigo


class NotaCorte(models.Model):
    matricula_curso = models.ForeignKey(MatriculaCurso)
    corte = models.ForeignKey(Corte)
    nota = models.FloatField(blank=True, null=True, validators=[validar_nota])
    fallas = models.IntegerField(help_text="Número de fallas durante el corte.", blank=True, null=True, validators=[MinValueValidator(0)])
    comportamiento = models.CharField(max_length=1, choices=TIPO_COMPORTAMIENTO, blank=True)
    
    
 

  
class HorarioCurso(models.Model):
    curso = models.ForeignKey(Curso)
    dia = models.CharField(verbose_name='Día', max_length=1, choices=DIAS) 
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    salon = models.ForeignKey(Salon, verbose_name='Salón')


class SesionCurso(models.Model):
    codigo = models.CharField(verbose_name='Código', max_length=200)
    curso = models.ForeignKey(Curso)
    fecha = models.DateField(blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
  
    def __unicode__(self):
        return self.codigo


class Asistencia(models.Model):
    sesion_curso = models.ForeignKey(SesionCurso)
    inscripcion_estudiante = models.ForeignKey(InscripcionEstudiante)
    asistio = models.BooleanField(verbose_name='Asistío', default=True)
    observaciones = models.TextField(max_length=200, blank=True)