# -*- coding: utf-8 -*-
from django.db import models
from academico.models import InscripcionEstudiante

# TODO: Leer configuracion desde un archivo externo,
# p.e., valores de constantes.
# http://docs.python.org/library/configparser.html

ESTADO_MATRICULA_FINANCIERA = (
  ('A', 'Activo'),
  ('E', 'Egresado'),
  ('X', 'Expulsado'),
  ('R', 'Retirado'),
  ('P', 'Suspendido por pago'),
)

class MatriculaFinanciera(models.Model):
  # Informacion general
  inscripcion_estudiante = models.ForeignKey(InscripcionEstudiante)
  fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
  estado = models.CharField(max_length=1, 
                            choices=ESTADO_MATRICULA_FINANCIERA, 
                            default='A')
  becado = models.BooleanField(help_text="Indica si el estudiante recibe o no beca.")
  valor_matricula = models.FloatField(verbose_name='Valor matrícula')
  valor_inscripcion = models.FloatField(verbose_name='Valor Inscripción')
  cuotas = models.IntegerField( help_text="Número de cuotas a diferir el valor de la matrícula.", 
                                default=1)
  cancelada = models.BooleanField(help_text='Indica si no existen deudas.')
  
  def __unicode__(self):
    return self.inscripcion_estudiante


class Pago(models.Model):
  matricula_financiera = models.ForeignKey(MatriculaFinanciera)
  fecha_pago = models.DateField()
  valor = models.FloatField()
  recibo_caja = models.CharField(max_length=200)
  observaciones = models.TextField(max_length=200, blank=True)
  
  
class Letra(models.Model):
  matricula_financiera = models.ForeignKey(MatriculaFinanciera)
  fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
  fecha_vencimiento = models.DateField()
  valor = models.FloatField()
  fecha_pago = models.DateField()
  cancelada = models.BooleanField(help_text='Indica si no existen deudas.')
  
  
class Multa(models.Model):
  matricula_financiera = models.ForeignKey(MatriculaFinanciera)
  fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
  valor = models.FloatField()
  concepto = models.TextField(max_length=200, blank=True)
  fecha_pago = models.DateField()
  cancelada = models.BooleanField(help_text='Indica si no existen deudas.')
  
  