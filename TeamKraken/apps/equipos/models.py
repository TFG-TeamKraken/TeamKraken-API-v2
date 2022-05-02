from django.db import models
from apps.authentication.models import User
from django.utils.timezone import *

# Create your models here.

class Equipo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    nombre_club = models.CharField(max_length=50, verbose_name='Nombre club')   # TODO implementar scraping
    temporada = models.CharField(max_length=20, verbose_name='Temporada')
    categoria = models.CharField(max_length=50, verbose_name='Categoria')
    domicilio = models.CharField(max_length=50, verbose_name='Domicilio')  # TODO implementar scraping
    localidad = models.CharField(max_length=50, verbose_name='Localidad')
    provincia = models.CharField(max_length=50, verbose_name='Provincia')
    codigo_postal = models.CharField(max_length=50, verbose_name='Código postal')
    cod_club = models.CharField(max_length=50, verbose_name='Código club', blank=True)  # TODO implementar scraping
    cod_equipo = models.CharField(max_length=50, verbose_name='Código equipo', blank=True)
    cod_temporada = models.CharField(max_length=50, verbose_name='Código temporada', blank=True)  # TODO implementar scraping
    cod_grupo = models.CharField(max_length=50, verbose_name='Código grupo', blank=True)  # TODO implementar scraping
    cod_competicion = models.CharField(max_length=50, verbose_name='Código competicion', blank=True)  # TODO implementar scraping
    creado_manual = models.BooleanField(verbose_name="Creado manualmente", default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # TODO eliminar scraping del email

    @property
    def id_equipo(self):
        años_temporada = self.temporada.split('-')
        temporada = ''.join(años_temporada)

        if len(self.cod_equipo) == 0:
            nombre_equipo = self.nombre.replace(" ", "")
            return ''.join([temporada, nombre_equipo])
        else:
            return ''.join([temporada, self.cod_equipo])


    def __str__(self):
        return self.nombre + " - " + self.categoria

class Nota(models.Model):
    fecha_creacion = models.DateField(verbose_name='Fecha de creación', default=now)
    texto = models.TextField(verbose_name='Texto')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.fecha_creacion) + " - " + str(self.equipo)