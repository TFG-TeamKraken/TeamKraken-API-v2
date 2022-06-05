from django.db import models

from apps.equipos.models import Equipo
from apps.jugadores.models import *
from apps.ejercicios.models import Ejercicio

# Create your models here.
class Entrenamiento(models.Model):
    NORMAL = 'Normal'
    FISICO = 'Fisico'
    RECUPERACION = 'Recuperacion'
    TIPO_ENTRENAMIENTO_CHOICES = [
        (NORMAL, 'Normal'),
        (FISICO, 'Fisico'),
        (RECUPERACION, 'Recuperacion'),
    ]
    fecha = models.DateField(verbose_name='Fecha')
    tipo_entrenamiento = models.CharField(max_length=30, choices=TIPO_ENTRENAMIENTO_CHOICES, default=NORMAL)
    ejercicios = models.ManyToManyField(Ejercicio, blank=True)
    jugadores = models.ManyToManyField(Jugador, blank=True)
    equipo = models.ForeignKey(Equipo , on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.fecha.__str__()


class DatosEntrenamiento(models.Model):
    minutos_entrenados = models.IntegerField(verbose_name='Minutos entrenados', default=0)
    plus_minutos_por_lesion = models.IntegerField(verbose_name='Plus de minutos entrenados si el jugador se ha marchado lesionado o con molestias', default=0)
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE, null=True)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, null=True)

    @property
    def plus_entrenamiento_fisico(self):
        " Devuelve un valor de 30 (minutos) si el entrenamiento padre ha sido un entrenamiento físico. Este valor luego se SUMA a los minutos entrenados en el serializador "
        if self.entrenamiento.tipo_entrenamiento == 'Fisico':
            return 30
        else:
            return 0

    @property
    def rec_entrenamiento_recuperacion(self):
        " Devuelve un valor de 30 (minutos) si el entrenamiento padre ha sido un entrenamiento de recuperación. Este valor luego se RESTA a los minutos entrenados en el serializador "
        if self.entrenamiento.tipo_entrenamiento == 'Recuperacion':
            return 30
        else:
            return 0
            
    def __str__(self):
        return self.entrenamiento.fecha.__str__()

class FaltaAsistencia(models.Model):
    INJUSTIFICADA = 'Injustificada'
    JUSTIFICADA = 'Justificada'
    LESION = 'Lesion'
    TIPO_FALTA_CHOICES = [
        (INJUSTIFICADA, 'Injustificada'),
        (JUSTIFICADA, 'Justificada'),
        (LESION, 'Lesion'),
    ]
    tipo = models.CharField(max_length=30, choices=TIPO_FALTA_CHOICES, default=INJUSTIFICADA)
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE, null=True)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.tipo