from attr import fields
from rest_framework import serializers

from .models import *

class ListaEntrenamientosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entrenamiento
        fields = (
            'id',
            'fecha',
            'tipo_entrenamiento'
        )

class ListaAsistentesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jugador
        fields = (
            'id',
            'nombre',
            'apellidos'
        )

class ListaEjerciciosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ejercicio
        fields = (
            'id',
            'nombre',
            'intensidad',
            'duracion',
            'descripcion'
        )

class ListaInformesSerializer(serializers.ModelSerializer):

    jugador = ListaAsistentesSerializer()

    class Meta:
        model = DatosEntrenamiento
        fields = (
            'id',
            'minutos_entrenados',
            'plus_minutos_por_lesion',
            'jugador',
        )

class JugadorFaltaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jugador
        fields = (
            'id',
            'nombre',
            'apellidos'
        )


class ListaFaltasAsistenciaSerializer(serializers.ModelSerializer):

    jugador = JugadorFaltaSerializer()

    class Meta:
        model = FaltaAsistencia
        fields = (
            'id',
            'tipo',
            'jugador'
        )

class DetallesEntrenamientoSerializer(serializers.ModelSerializer):

    jugadores = ListaAsistentesSerializer(many=True)
    ejercicios = ListaEjerciciosSerializer(many=True)
    informes = serializers.SerializerMethodField()
    faltas = serializers.SerializerMethodField()

    class Meta:
        model = Entrenamiento
        fields = (
            'id',
            'fecha',
            'tipo_entrenamiento',
            'jugadores',
            'ejercicios',
            'informes',
            'faltas'
        )

    def get_informes(self, obj):
        query = DatosEntrenamiento.objects.filter(entrenamiento__id=obj.id)
        informes_serializados = ListaInformesSerializer(query, many=True).data
        return informes_serializados

    def get_faltas(self, obj):
        query = FaltaAsistencia.objects.filter(entrenamiento__id=obj.id)
        faltas_serializadas = ListaFaltasAsistenciaSerializer(query, many=True).data
        return faltas_serializadas


class NuevoEntrenamientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entrenamiento
        fields = (
            'fecha',
            'tipo_entrenamiento',
            'ejercicios',
            'jugadores',
            'equipo'
        )

class EditEntrenamientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entrenamiento
        fields = (
            'fecha',
        )


class InformeSerializer(serializers.ModelSerializer):

    jugador = ListaAsistentesSerializer()
    entrenamiento = ListaEntrenamientosSerializer()

    class Meta:
        model = DatosEntrenamiento
        fields = (
            'id',
            'minutos_entrenados',
            'plus_minutos_por_lesion',
            'plus_entrenamiento_fisico',
            'rec_entrenamiento_recuperacion',
            'entrenamiento',
            'jugador',
        )

class CrearActualizarEliminarDetallesInformesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DatosEntrenamiento
        fields = (
            'id',
            'minutos_entrenados',
            'plus_minutos_por_lesion',
            'plus_entrenamiento_fisico',
            'rec_entrenamiento_recuperacion',
            'entrenamiento',
            'jugador',
        )