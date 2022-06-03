from django.db import models

from apps.authentication.models import User

# Create your models here.
class ObjetivoTecnico(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Objetivo técnico')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class ObjetivoTactico(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Objetivo táctico')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class ObjetivoFisico(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Objetivo físico')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class ObjetivoPsicologico(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Objetivo Psicológico')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class ObjetivoEspecifico(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Objetivo Específico')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Ejercicio(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    material = models.TextField(verbose_name='Material', help_text='Enumera el material necesario')
    objetivo_tecnico = models.ManyToManyField(ObjetivoTecnico, blank=True)
    objetivo_tactico = models.ManyToManyField(ObjetivoTactico, blank=True)
    objetivo_fisico = models.ManyToManyField(ObjetivoFisico, blank=True)
    objetivo_psicologico = models.ManyToManyField(ObjetivoPsicologico, blank=True)
    objetivo_especifico = models.ManyToManyField(ObjetivoEspecifico, blank=True)
    descripcion = models.TextField(verbose_name='Descripción', help_text='Añade una descripción')
    consejos = models.TextField(verbose_name='Consejos', help_text='Consejos')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nombre