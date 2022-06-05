from django.contrib import admin

from apps.entrenamientos.models import *

# Register your models here.

admin.site.register(Entrenamiento)
admin.site.register(DatosEntrenamiento)
admin.site.register(FaltaAsistencia)