from rest_framework import serializers

from apps.authentication.serializers import UserSerializer

from .models import *

class ListaEquiposSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipo
        fields = (
            'id',
            'nombre',
            'categoria',
            'temporada'
        )


class EquipoSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    notas = serializers.SerializerMethodField()
    # TODO faltan jugadores

    class Meta:
        model = Equipo
        fields = (
            'id_equipo',
            'nombre',
            'nombre_club',
            'temporada',
            'categoria',
            'domicilio',
            'localidad',
            'provincia',
            'codigo_postal',
            'cod_club',
            'cod_equipo',
            'cod_temporada',
            'cod_grupo',
            'cod_competicion',
            'creado_manual',
            'user',
            'notas'
        )

    def get_notas(self, obj):
        query = Nota.objects.filter(equipo__id=obj.id)
        notas_serializadas = ListaNotasSerializer(query, many=True).data
        return notas_serializadas

class ListaNotasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nota
        fields = (
            'id',
            'fecha_creacion',
            'texto'
        )

class NotaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nota
        fields = (
            'id',
            'fecha_creacion',
            'texto',
            'equipo'
        )