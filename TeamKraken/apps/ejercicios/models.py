from django.db import models

from apps.authentication.models import User

# Create your models here.
class ObjetivoTecnico(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Objetivo técnico')

    def __str__(self):
        return self.nombre
    
class ObjetivoTactico(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Objetivo táctico')

    def __str__(self):
        return self.nombre

class ObjetivoFisico(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Objetivo físico')

    def __str__(self):
        return self.nombre

class ObjetivoPsicologico(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Objetivo Psicológico')

    def __str__(self):
        return self.nombre

class ObjetivoEspecifico(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Objetivo Específico')

    def __str__(self):
        return self.nombre
    
class Ejercicio(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    materiales = models.TextField(verbose_name='Material', help_text='Enumera el material necesario')
    representacion = models.CharField(verbose_name='Representación', max_length=100, blank=True)
    edad_recomendada = models.CharField(verbose_name='Edad recomendada', max_length=100, blank=True)
    dificultad = models.CharField(verbose_name='Dificultad', max_length=100, blank=True)
    intensidad = models.CharField(verbose_name='Intensidad', max_length=100, blank=True)
    duracion = models.CharField(verbose_name='Duración', max_length=100, blank=True)
    objetivo_tecnico = models.ManyToManyField(ObjetivoTecnico, blank=True)
    objetivo_tactico = models.ManyToManyField(ObjetivoTactico, blank=True)
    objetivo_fisico = models.ManyToManyField(ObjetivoFisico, blank=True)
    objetivo_psicologico = models.ManyToManyField(ObjetivoPsicologico, blank=True)
    objetivo_especifico = models.ManyToManyField(ObjetivoEspecifico, blank=True)
    descripcion = models.TextField(verbose_name='Descripción', help_text='Añade una descripción', blank=True)
    consejos = models.TextField(verbose_name='Consejos', help_text='Consejos', blank=True)
    created_by_user = models.BooleanField(verbose_name='Creado por el usuario', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nombre