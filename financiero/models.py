# -*- coding: utf-8 -*-
from django.db import models
from academico.models import MatriculaCiclo, Profesor, Curso, Programa, Ciclo
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ModelForm, TextInput

class CalendarioPago(models.Model):
    ciclo = models.ForeignKey(Ciclo)
    programa = models.ManyToManyField(Programa, symmetrical=False)
    
    def plazos(self):
        return len(Plazo.objects.filter(calendario_pago=self))
    
    def programas(self):
        return len(self.programa.all())
         
    def __unicode__(self):
        return u'%s' % (self.ciclo)
    

class MatriculaFinanciera(models.Model):
    fecha_matricula = models.DateField()
    matricula_ciclo = models.ForeignKey(MatriculaCiclo, unique=True)
    calendario_pago = models.ForeignKey(CalendarioPago)
    
    valor_inscripcion = models.FloatField(verbose_name="Valor inscripción", 
                                    blank=True, 
                                    null=True, 
                                    default=0, 
                                    validators=[MinValueValidator(0)])
    valor_matricula = models.FloatField(help_text="Representa el costo de matrícula al programa menos el valor de descuento.", 
                                        verbose_name='Valor matrícula', 
                                        blank=True, 
                                        null=True, 
                                        default=0, 
                                        validators=[MinValueValidator(0)])
    descuento = models.FloatField(help_text="Descuento sobre valor matrícula.", 
                                  blank=True, 
                                  null=True, 
                                  default=0, 
                                  validators=[MinValueValidator(0)])
    
    valor_abonado = models.FloatField(help_text="Valor abonado a la fecha.", 
                                      blank=True, 
                                      null=True, 
                                      default=0, 
                                      validators=[MinValueValidator(0)])
    paz_y_salvo = models.BooleanField()
        
    def __unicode__(self):
        return "%s" %(self.matricula_ciclo)
        
    
    def codigo_estudiante(self):
        return "%s" %(self.matricula_ciclo.codigo_estudiante())
    
    def nombre_estudiante(self):
        return "%s" %(self.matricula_ciclo.nombre_estudiante())
    
    def id_programa(self):
        return "%s" %(self.matricula_ciclo.id_programa())
    
    def nombre_programa(self):
        return "%s" %(self.matricula_ciclo.nombre_programa())
    
    def cursos_inscritos(self):
        '''
        Retorna el número de cursos que está tomando en el ciclo
        '''
        return self.matricula_ciclo.cursos_inscritos()
    
    def cancelar(self):
        pagos = Pago.objects.filter(matricula_financiera = self.id)
        valor = 0
        for pago in pagos:
            valor = valor + pago.valor
        if valor >= self.valor_matricula:
            self.paz_y_salvo = True
        else:
            self.paz_y_salvo = False
        self.valor_abonado = valor
        self.save()
    
    def saldo(self):
        return self.valor_matricula - self.valor_abonado
        
    def save(self, *args, **kwargs):
        try:
            costo_programa = CostoPrograma.objects.get(programa = self.matricula_ciclo.matricula_programa.programa)
            creditos_cursados = self.matricula_ciclo.total_creditos()
            costo_programa_creditos = creditos_cursados * costo_programa.valor_credito
            # Maximo entre el valor del programa basico y por creditos
            subtotal = max(costo_programa_creditos, costo_programa.valor) 
            valor = subtotal - self.descuento
        except CostoPrograma.DoesNotExist:
            valor = -5
            
        self.valor_matricula = valor
        super(MatriculaFinanciera, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Matrículas financieras"
        verbose_name = "Matrícula financiera"
        

class Pago(models.Model):
    matricula_financiera = models.ForeignKey(MatriculaFinanciera)
    fecha_pago = models.DateField(blank=True, null=True)
    valor = models.FloatField(validators=[MinValueValidator(0)])
    concepto = models.TextField(max_length=200, blank=True)
    
    def save(self, *args, **kwargs):
        super(Pago, self).save(*args, **kwargs)
        self.matricula_financiera.cancelar()
        
    def delete(self, *args, **kwargs):
        super(Pago, self).delete(*args, **kwargs)
        self.matricula_financiera.cancelar()
        
    def nombre_programa(self):
        return u"%s" %(self.matricula_financiera.nombre_programa())
    
    def __unicode__(self):
        return "%s" % self.valor
  

class CostoPrograma(models.Model):
    ciclo = models.ForeignKey(Ciclo)
    programa = models.ManyToManyField(Programa, symmetrical=False)
    valor = models.FloatField(default=0)
    valor_credito = models.FloatField(default=0, help_text="Valor de cada crédito académico.")
    
    def programas(self):
        return "%s" %(len(self.programa.all()))

 
  
class HoraCatedra(models.Model):
    profesor = models.ForeignKey(Profesor)
    ciclo = models.ForeignKey(Ciclo)
    tiempo_hora = models.PositiveIntegerField(default=60, 
                                              help_text="Indica el tiempo de hora cátedra en minutos.")
    valor_hora = models.FloatField(default=0, 
                                   validators=[MinValueValidator(0)])
    observaciones = models.TextField(max_length=200, 
                                     blank=True)
        
    class Meta:
        verbose_name_plural = 'horas cátedra'
        verbose_name = 'hora cátedra'
    
    def __unicode__(self):
        return "%s" %(self.id)
    
    def nombre_profesor(self):
        return self.profesor.nombre()


class HoraCatedraForm(ModelForm):
    class Meta:
        model = HoraCatedra


class Adelanto(models.Model):
    hora_catedra = models.ForeignKey(HoraCatedra)
    fecha_adelanto = models.DateField()
    valor = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fecha_retorno = models.DateField()
    concepto = models.TextField(max_length=200, blank=True) 
    cancelada = models.BooleanField(help_text='Indica si no existen deudas por adelanto.')
    
    def __unicode__(self):
        return "%s" %(self.fecha_adelanto)
       
    
class Sesion(models.Model):
    hora_catedra = models.ForeignKey(HoraCatedra)
    curso = models.ForeignKey(Curso)
    fecha_sesion = models.DateField(verbose_name='Fecha sesión')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tiempo_planeado = models.PositiveIntegerField(help_text='Tiempo esperado de duración de sesión en minutos', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Sesiones'
        verbose_name = 'Sesión'
   
   
class Descuento(models.Model):
    hora_catedra = models.ForeignKey(HoraCatedra)
    concepto = models.CharField(max_length=200, blank=True)
    porcentaje = models.PositiveIntegerField(max_length=2)
    
    def __unicode__(self):
        return "%s" %(self.porcenaje)

#class LiquidarPago(models.Model):
#    hora_catedra = models.ForeignKey(HoraCatedra)
#    recibo = models.CharField(max_length=20, unique=True, help_text="Número de recibo")
#    fecha_liquidacion = models.DateField(verbose_name='Fecha liquidación')
#    fecha_inicio = models.DateField(verbose_name='Fecha inicio')
#    fecha_fin = models.DateField(verbose_name='Fecha fin')
#    horas_sesiones = models.PositiveIntegerField(help_text='Horas de clase', blank=True, null=True)
#    valor_liquidado = models.FloatField(default=0, validators=[MinValueValidator(0)], blank=True, null=True)
#    valor_adelanto = models.FloatField(default=0, validators=[MinValueValidator(0)], blank=True, null=True)
#    valor_descuento = models.FloatField(default=0, validators=[MinValueValidator(0)], blank=True, null=True)
#    
#    def valor_total(self):
#        return self.valor_liquidado - (self.valor_adelanto + self.valor_descuento)
        
#class LiquidarPagoForm(ModelForm):
#    class Meta:
#        model = LiquidarPago
#        widgets = {'fecha_liquidacion': TextInput(attrs={'class':'vDateField'}),
#                   'fecha_inicio': TextInput(attrs={'class':'vDateField'}),
#                   'fecha_fin': TextInput(attrs={'class':'vDateField'})}

        
class Plazo(models.Model):
    calendario_pago = models.ForeignKey(CalendarioPago)
    fecha_ordinaria = models.DateField()
    fecha_extraordinaria = models.DateField()
    porcentaje_incremento = models.IntegerField(default=0, 
                                         validators=[MinValueValidator(0), MaxValueValidator(100)] )
    
    def __unicode__(self):
        return u'%s - %s' % (self.fecha_ordinaria, 
                                  self.fecha_extraordinaria)