from sqlite3 import Date
from django.db import models
from apps.authentication.models import User
from django.utils.timezone import *

# Create your models here.

class Equipo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    codigo = models.CharField(max_length=50, verbose_name='Codigo')
    domicilio = models.CharField(max_length=50, verbose_name='Domicilio')
    codigo_postal = models.CharField(max_length=50, verbose_name='Codigo postal')
    localidad = models.CharField(max_length=50, verbose_name='Localidad')
    provincia = models.CharField(max_length=50, verbose_name='Provincia')
    categoria = models.CharField(max_length=50, verbose_name='Categoria')
    email = models.CharField(max_length=50, verbose_name='Email')
    temporada = models.CharField(max_length=20, verbose_name='Temporada')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nombre + ", " + self.localidad + "(" + self.provincia + ")"

class Nota(models.Model):
    fecha_creacion = models.DateField(verbose_name='Fecha de creación', default=now)
    texto = models.TextField(verbose_name='Texto', max_length="500")
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True, blank=True)