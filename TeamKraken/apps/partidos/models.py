from django.db import models
from apps.partidos.managers import DatosPartidoManager
from apps.jugadores.models import Posicion
from apps.equipos.models import Equipo
from apps.jugadores.models import Jugador
from django.utils.timezone import *

# Create your models here.

class Partido(models.Model):
    fecha = models.DateField(verbose_name='Fecha')
    temporada = models.CharField(max_length=50, verbose_name='Temporada', default=str(now().year) + "-" + str(now().year + 1))
    local = models.CharField(max_length=50, verbose_name='Local')
    visitante = models.CharField(max_length=50, verbose_name='Visitante')
    goles_local = models.IntegerField(verbose_name='Goles equipo local')
    goles_visitante = models.IntegerField(verbose_name='Goles equipo visitante')
    convocados = models.ManyToManyField(Jugador)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.local + " - " + self.visitante
    
class DatosPartido(models.Model):
    titular = models.BooleanField(verbose_name='Titular', default=False)
    valoracion_partido = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Valoración del partido realizado', blank=True, null=True)
    posicion_jugada = models.ForeignKey(Posicion, on_delete=models.SET_NULL, verbose_name='Posición en la que ha jugado', blank=True, null=True)
    tiros_puerta = models.IntegerField(verbose_name='Tiros a puerta', blank=True, null=True)
    goles = models.IntegerField(verbose_name='Goles', blank=True, null=True)
    asistencias = models.IntegerField(verbose_name='Asistencias', blank=True, null=True)
    paradas = models.IntegerField(verbose_name='Paradas (sólo porteros)', blank=True, null=True)
    goles_encajados = models.IntegerField(verbose_name='Goles encajados (sólo porteros)', blank=True, null=True)
    robos_balon = models.IntegerField(verbose_name='Robos de balon', blank=True, null=True)
    balones_perdidos = models.IntegerField(verbose_name='Balones perdidos', blank=True, null=True)
    pases_cortados = models.IntegerField(verbose_name='Balones recuperados', blank=True, null=True)
    minutos_jugados = models.IntegerField(verbose_name='Minutos jugados', default=0)
    plus_minutos_por_lesion = models.IntegerField(verbose_name='Plus de minutos jugados si el jugador se ha marchado lesionado o con molestias', default=0)
    amarillas = models.IntegerField(verbose_name='Amarillas', blank=True, null=True)
    rojas = models.IntegerField(verbose_name='Rojas', blank=True, null=True)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, null=True)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, null=True)

    objects = DatosPartidoManager()
    
    def __str__(self):
        return self.jugador.nombre + " " + self.jugador.apellidos + " (" + self.partido.local + " - " + self.partido.visitante + ")"
    