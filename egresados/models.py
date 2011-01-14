# -*- coding: utf-8 -*-
from django.db import models
import datetime

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

NIVELES_CARGOS = (
    ('A',  'Alta gerencia'),
    ('G',  'Gerencia media'),
    ('P',  'Profesional'),
    ('S',  'Asistencial'),               
)

SALARIOS = (
    ('A',  '$   500.001 - $ 1.000.000'),
    ('B',  '$ 1.000.001 - $ 1.500.000'),
    ('C',  '$ 1.500.001 - $ 2.000.000'),
    ('D',  '$ 2.000.001 - $ 2.500.000'),
    ('E',  '$ 2.500.001 - $ 3.000.000'),
    ('F',  '$ 3.000.001 - $ 3.500.000'),
    ('G',  '$ 3.500.001 - $ 4.000.000'),
    ('H',  '$ 4.000.001 - Más        '),
)

SECTORES = (
    ('A',  'Alimentos'),
    ('B',  'Asegurador'),
    ('C',  'Bebidas y tabaco'),
    ('D',  'Comercio al por menor'),
    ('E',  'Construcción'),
    ('F',  'Consultorías / Asesorías'),
    ('G',  'Consumo masivo'),
    ('H',  'Editorial e impresión'),
    ('I',  'Educativo'),
    ('J',  'Energético'),
    ('K',  'Entretenimiento'),
    ('L',  'Financiero'),
    ('M',  'Manufactura'),
    ('N',  'Minería, hierro, acero y otros materiales'),
    ('O',  'Plástico y caucho'),
    ('P',  'Químicos'),
    ('Q',  'Salud'),
    ('R',  'Servicios'),
    ('S',  'Tecnología'),
    ('T',  'Telecomunicaciones'),
    ('U',  'Transporte'),
    ('V',  'Vehículos y partes'),
    ('W',  'Otros'),
)

class Egresado(models.Model):
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
    
    # Informacion de contacto
    direccion = models.CharField( verbose_name='Dirección', max_length=200, blank=True)
    lugar_residencia = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(verbose_name='Teléfono', max_length=200, blank=True)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)
    
    # Informacion de acceso
    usuario = models.CharField(max_length=50, blank=True)
    contrasena = models.CharField(verbose_name='Contraseña', max_length=200, blank=True)
    
    def __unicode__(self):
        return self.documento

class HojaVida(models.Model):
    egresado = models.ForeignKey(Egresado)
    titulo = models.CharField(max_length=200)
    publica = models.BooleanField(default=True)
    ultima_modificacion = models.DateTimeField()
    
    def __unicode__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'hoja de vida'
        verbose_name_plural = 'hojas de vida'
    

class Estudio(models.Model):
    hoja_vida = models.ForeignKey(HojaVida)
    tipo_estudio = models.CharField(max_length=1, choices=TIPO_ESTUDIO, blank=True) 
    institucion = models.CharField( verbose_name='Institución', max_length=200, blank=True)
    titulo = models.CharField(verbose_name='Título', max_length=200, blank=True)
    fecha_graduacion = models.DateField(verbose_name='Fecha graduación', blank=True, null=True)
    actualmente = models.BooleanField()
    
class Idioma(models.Model):
    hoja_vida = models.ForeignKey(HojaVida)
    idioma = models.CharField(max_length=50, blank=True)
    lee = models.IntegerField()
    escribe = models.IntegerField()
    habla = models.IntegerField()

class ExperienciaLaboral(models.Model):
    hoja_vida = models.ForeignKey(HojaVida)
    cargo = models.CharField(max_length=200, blank=True)
    empresa = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(max_length=200, blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    actualmente = models.BooleanField()

class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=200, blank=True)
    pais = models.CharField(verbose_name='País', max_length=200, blank=True)
    telefono = models.CharField(max_length=200, blank=True)
    fax = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique = True, blank=True)
    web = models.URLField(blank=True)
    
    def __unicode__(self):
        return self.nombre
    
    
    
class Oferta(models.Model):
    empresa = models.ForeignKey(Empresa)
    codigo = models.CharField(verbose_name='Código', max_length=200)
    titulo = models.CharField(verbose_name='Título', max_length=200)
    descripcion = models.TextField(verbose_name='Descripción', max_length=200, blank=True)
    requisitos = models.TextField(max_length=200, blank=True)
    nivel_cargo = models.CharField(max_length=1, choices=NIVELES_CARGOS, blank=True) 
    sector = models.CharField(max_length=1, choices=SECTORES, blank=True)
    salario = models.CharField(max_length=1, choices=SALARIOS, blank=True)
    
    ciudad = models.CharField(max_length=200, blank=True)
    pais = models.CharField(verbose_name='País', max_length=200, blank=True)
    
    fecha_publicacion = models.DateField(verbose_name='Fecha publicación')
    fecha_cierre = models.DateField()
    
    def vigente(self):
        return self.fecha_cierre >= datetime.date.today()
    
    def __unicode__(self):
        return self.codigo