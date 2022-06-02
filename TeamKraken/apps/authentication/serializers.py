from rest_framework import serializers

from apps.equipos.models import Equipo

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

class UserSerializer(serializers.ModelSerializer):

    equipos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'equipos'
        )

    def get_equipos(self, obj):
        query = Equipo.objects.filter(user__id=obj.id)
        equpos_serializados = ListaEquiposSerializer(query, many=True).data
        return equpos_serializados