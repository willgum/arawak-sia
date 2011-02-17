# -*- coding: utf-8 -*-
from django.db import models
from academico.models import MatriculaPrograma, MatriculaCiclo, Profesor, Curso, Programa, Ciclo
from django.core.validators import MinValueValidator

class InscripcionPrograma(models.Model):
    matricula_programa = models.OneToOneField(MatriculaPrograma)
    fecha_inscripcion = models.DateField(verbose_name='Fecha de inscripción')
    valor_inscripcion = models.FloatField(help_text="Representa el costo de inscripción al programa.", verbose_name='Valor inscripción', default=0, validators=[MinValueValidator(0)])
    fecha_pago = models.DateField(verbose_name='Fecha de pago', blank=True, null=True)
    
    def __unicode__(self):
        return "%s" %(self.matricula_programa.codigo)
    
    class Meta:
        verbose_name_plural = 'Inscripciones programa'
        verbose_name = 'Inscripción programa'
        
    def codigo_estudiante(self):
        return "%s" %(self.matricula_programa.codigo)
    
    def nombre_estudiante(self):
        return "%s" %(self.matricula_programa.nombre_estudiante())
    
    def id_programa(self):
        return "%s" %(self.matricula_programa.programa.id)
    
    def nombre_programa(self):
        return "%s" %(self.matricula_programa.nombre_programa())

    
class MatriculaFinanciera(models.Model):
    # Informacion general
    inscripcion_programa = models.ForeignKey(InscripcionPrograma)
    matricula_ciclo = models.ForeignKey(MatriculaCiclo, limit_choices_to = {'matricula_programa__programa__id': 1})
    fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
    becado = models.BooleanField(help_text="Indica si el estudiante recibe o no beca.")
    valor_descuento = models.FloatField(help_text="Indica el valor de descuento sobre el costo de matrícula.", verbose_name='Valor descuento', blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    valor_matricula = models.FloatField(help_text="Representa el costo de matrícula al programa menos el valor de descuento.", verbose_name='Valor matrícula', blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    valor_abonado = models.FloatField(help_text="Corresponde al valor abonado al costo de matrícula a la fecha.", verbose_name='Valor abonado', blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    cuotas = models.IntegerField(help_text="Número de cuotas a diferir el valor de la matrícula.", default=1)
    paz_y_salvo = models.BooleanField(help_text='Indica si no existen deudas.')
    
    class Meta:
        verbose_name_plural = 'Matrículas financieras'
        verbose_name = 'Matrícula financiera'
        
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
            self.paz_y_salvo = True
        else:
            self.paz_y_salvo = False
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
    valor = models.FloatField(validators=[MinValueValidator(0)])
    recibo_caja = models.CharField(max_length=200)
    concepto = models.TextField(max_length=200, blank=True)
    
  
class Letra(models.Model):
    matricula_financiera = models.ForeignKey(MatriculaFinanciera)
    fecha_expedicion = models.DateField(verbose_name='Fecha expedición')
    fecha_vencimiento = models.DateField()
    valor = models.FloatField(validators=[MinValueValidator(0)])
    fecha_pago = models.DateField(blank=True, null=True)
    cancelada = models.BooleanField(help_text='Indica si no existen deudas.')
    
    def save(self, *args, **kwargs):
        super(Letra, self).save(*args, **kwargs)
        self.matricula_financiera.cancelar()
        
    def delete(self, *args, **kwargs):
        super(Letra, self).delete(*args, **kwargs)
        self.matricula_financiera.cancelar()
  
class HoraCatedra(models.Model):
    profesor = models.ForeignKey(Profesor)
    ciclo = models.ForeignKey(Ciclo)
    valor_hora = models.FloatField(default=0, validators=[MinValueValidator(0)])
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
    
class Sesion(models.Model):
    hora_catedra = models.ForeignKey(HoraCatedra)
    curso = models.ForeignKey(Curso)
    fecha = models.DateField(verbose_name='Fecha sesión de curso')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tiempo_planeado = models.IntegerField(help_text='Tiempo esperado de duración de sesión en minutos', default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name_plural = 'Sesiones'
        verbose_name = 'Sesión'
    