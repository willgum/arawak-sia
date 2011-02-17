# -*- coding: utf-8 -*-
from django.db import models
from academico.models import MatriculaCiclo, Profesor, Curso, Programa, Ciclo


class MatriculaFinanciera(models.Model):
    # Informacion general
    matricula_ciclo = models.ForeignKey(MatriculaCiclo)
    fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
    becado = models.BooleanField(help_text="Indica si el estudiante recibe o no beca.")
    valor_descuento = models.FloatField(verbose_name='Valor descuento', blank=True, null=True, default=0)
    valor_matricula = models.FloatField(verbose_name='Valor matrícula', blank=True, null=True, default=0)
    valor_abonado = models.FloatField(verbose_name='Valor abonado', blank=True, null=True, default=0)
    cuotas = models.IntegerField(help_text="Número de cuotas a diferir el valor de la matrícula.", default=1)
    cancelada = models.BooleanField(help_text='Indica si no existen deudas.')
    
    def __unicode__(self):
        return "%s" %(self.matricula_ciclo.codigo_ciclo())
    
    def codigo_estudiante(self):
        return "%s" %(self.matricula_ciclo.codigo_estudiante())
    
    def nombre_estudiante(self):
        return "%s" %(self.matricula_ciclo.nombre_estudiante())
    
    def id_programa(self):
        return "%s" %(self.matricula_ciclo.matricula_programa.programa.id)
    
    def nombre_programa(self):
        return "%s" %(self.matricula_ciclo.nombre_programa())
    
    def inscripcion_ciclo(self):
        return "%s" %(self.matricula_ciclo.codigo_ciclo())
    
    def cancelar(self):
        pagos = Letra.objects.filter(matricula_financiera = self.id)
        valor = 0
        for pago in pagos:
            if pago.cancelada==True:
                valor = valor + pago.valor
        if valor >= self.valor_matricula:
            self.cancelada = True
        else:
            self.cancelada = False
        self.valor_abonado = valor
        self.save()
        
    def save(self, *args, **kwargs):
        try:
            costo_programa = CostoPrograma.objects.get(programa = self.matricula_ciclo.matricula_programa.programa)
            valor = costo_programa.valor - self.valor_descuento
        except CostoPrograma.DoesNotExist:
            valor = 0
            
        self.valor_matricula = valor
        super(MatriculaFinanciera, self).save(*args, **kwargs)
        
        


class Pago(models.Model):
    matricula_financiera = models.ForeignKey(MatriculaFinanciera)
    fecha_pago = models.DateField()
    valor = models.FloatField()
    recibo_caja = models.CharField(max_length=200)
    concepto = models.TextField(max_length=200, blank=True)
    
  
class Letra(models.Model):
    matricula_financiera = models.ForeignKey(MatriculaFinanciera)
    fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
    fecha_vencimiento = models.DateField()
    valor = models.FloatField(default=0)
    fecha_pago = models.DateField()
    cancelada = models.BooleanField(help_text='Indica si no existen deudas.')
    
    def save(self, *args, **kwargs):
        super(Letra, self).save(*args, **kwargs)
        self.matricula_financiera.cancelar()
        
    def delete(self, *args, **kwargs):
        super(Letra, self).delete(*args, **kwargs)
        self.matricula_financiera.cancelar()
  
class Multa(models.Model):
    matricula_financiera = models.ForeignKey(MatriculaFinanciera)
    fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
    valor = models.FloatField()
    concepto = models.TextField(max_length=200, blank=True)
    fecha_pago = models.DateField()
    cancelada = models.BooleanField(help_text='Indica si no existen deudas.')
  

class HoraCatedra(models.Model):
    profesor = models.ForeignKey(Profesor)
    curso = models.ForeignKey(Curso)
    valor_hora = models.FloatField(blank=True, null=True)
    observaciones = models.TextField(max_length=200, blank=True)
  
    class Meta:
        verbose_name_plural = 'horas cátedra'
        verbose_name = 'hora cátedra'
        
class CostoPrograma(models.Model):
    programa = models.ForeignKey(Programa)
    ciclo = models.ForeignKey(Ciclo)
    valor = models.FloatField(default=0)
    
    def nombre_programa(self):
        return "%s" %(self.programa.nombre)
    
    def codigo_ciclo(self):
        return "%s" %(self.ciclo.codigo)