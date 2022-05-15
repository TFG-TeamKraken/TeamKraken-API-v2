from django.db import models

from apps.equipos.models import Equipo

# Create your models here.

class Posicion(models.Model):
    abreviacion = models.CharField(max_length=3, verbose_name='Abreviación')
    nombre = models.CharField(max_length=30, verbose_name='Nombre')

    def __str__(self):
        return self.abreviacion


class Jugador(models.Model):
    PIE_DERECHO = 'PD'
    PIE_IZQUIERDO = 'PI'
    AMBIDIESTRO = 'AM'
    PIE_DOMINANTE_CHOICES = [
        (PIE_DERECHO, 'Pie derecho'),
        (PIE_IZQUIERDO, 'Pie izquierdo'),
        (AMBIDIESTRO, 'Ambidiestro'),
    ]
    nombre = models.CharField(max_length=30, verbose_name='Nombre')
    apellidos = models.CharField(max_length=50, verbose_name='Apellidos')
    fecha_nacimiento = models.CharField(max_length=50, verbose_name='Fecha de nacimiento', blank=True, null=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    posicion_principal = models.ForeignKey(Posicion, on_delete=models.SET_NULL, related_name='pos_principal_jugador', verbose_name='Posicion principal', blank=True, null=True)
    posiciones_secundarias = models.ManyToManyField(Posicion, related_name='pos_secundarias_jugador', verbose_name='Posiciones secundarias', blank=True)
    pie_dominante = models.CharField(max_length=2, choices=PIE_DOMINANTE_CHOICES, default=PIE_DERECHO, blank=True, null=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre + " " + self.apellidos


class Cooper(models.Model):
    fecha = models.DateField(verbose_name='Fecha')
    distancia = models.IntegerField(verbose_name='Distancia recorrida')
    vo2max = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='vo2max')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fecha.__str__() + " - " + self.jugador.nombre + " " + self.jugador.apellidos