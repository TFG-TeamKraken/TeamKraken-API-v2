
from rest_framework import serializers

from apps.ejercicios.models import *
from apps.authentication.serializers import UserSerializer

class ObjetivoTecnicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjetivoTecnico
        fields = (
            'id',
            'nombre'
        )

class ObjetivoTacticoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjetivoTactico
        fields = (
            'id',
            'nombre'
        )

class ObjetivoFisicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjetivoFisico
        fields = (
            'id',
            'nombre'
        )

class ObjetivoPsicologicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjetivoPsicologico
        fields = (
            'id',
            'nombre'
        )


class ObjetivoEspecificoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjetivoEspecifico
        fields = (
            'id',
            'nombre'
        )

class DetallesEjercicioSerializer(serializers.ModelSerializer):

    objetivo_tecnico = ObjetivoTecnicoSerializer(many=True)
    objetivo_tactico = ObjetivoTacticoSerializer(many=True)
    objetivo_fisico = ObjetivoFisicoSerializer(many=True)
    objetivo_psicologico = ObjetivoPsicologicoSerializer(many=True)
    objetivo_especifico = ObjetivoEspecificoSerializer(many=True)

    class Meta:
        model = Ejercicio
        fields = (
            'id',
            'nombre',
            'materiales',
            'consejos',
            'descripcion',
            'representacion',
            'edad_recomendada',
            'dificultad',
            'intensidad',
            'duracion',
            'objetivo_tecnico',
            'objetivo_tactico',
            'objetivo_fisico',
            'objetivo_psicologico',
            'objetivo_especifico',
            'created_by_user'
        )

class EjercicioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ejercicio
        fields = (
            'id',
            'nombre',
            'materiales',
            'consejos',
            'descripcion',
            'representacion',
            'edad_recomendada',
            'dificultad',
            'intensidad',
            'duracion',
            'objetivo_tecnico',
            'objetivo_tactico',
            'objetivo_fisico',
            'objetivo_psicologico',
            'objetivo_especifico',
            'created_by_user',
            'user'
        )


class FetchEjerciciosSerializer(serializers.Serializer):

    nombre = serializers.CharField()
    representacion = serializers.CharField()
    materiales = serializers.CharField()
    consejos = serializers.CharField()
    descripcion = serializers.CharField()
    edad_recomendada = serializers.CharField()
    dificultad = serializers.CharField()
    intensidad = serializers.CharField()
    duracion = serializers.CharField()
    objetivo_tecnico = serializers.ListField()
    objetivo_tactico = serializers.ListField()
    objetivo_fisico = serializers.ListField()
    objetivo_psicologico = serializers.ListField()
    objetivo_especifico = serializers.ListField()
    user = serializers.IntegerField()


class ListaNuevosEjerciciosSerializer(serializers.Serializer):

    ejercicios = EjercicioSerializer(many=True)


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


class FiltroEjerciciosSerializer(serializers.Serializer):
    
    nombre = serializers.CharField(required=False, allow_blank=True)
    edad_recomendada = serializers.CharField(required=False, allow_blank=True)
    intensidad = serializers.CharField(required=False, allow_blank=True)
    duracion = serializers.CharField(required=False, allow_blank=True)
    objetivo_tecnico = serializers.ListField()
    objetivo_tactico = serializers.ListField()
    objetivo_fisico = serializers.ListField()
    objetivo_psicologico = serializers.ListField()
    objetivo_especifico = serializers.ListField()


class QueryEjerciciosSerializer(serializers.Serializer):

    first = serializers.IntegerField()
    rows = serializers.IntegerField()
    filters = FiltroEjerciciosSerializer()