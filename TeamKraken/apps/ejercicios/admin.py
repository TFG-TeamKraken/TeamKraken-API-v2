from django.contrib import admin

from apps.ejercicios.models import *

# Register your models here.
admin.site.register(Ejercicio)
admin.site.register(ObjetivoTecnico)
admin.site.register(ObjetivoTactico)
admin.site.register(ObjetivoFisico)
admin.site.register(ObjetivoPsicologico)
admin.site.register(ObjetivoEspecifico)