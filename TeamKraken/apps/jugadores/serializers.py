from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from apps.partidos.models import Partido

from apps.partidos.models import DatosPartido

from .models import *

class PosicionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posicion
        fields = (
            'id',
            'abreviacion',
        )

class EquipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipo
        fields = (
            'id',
            'nombre',
            'categoria',
            'temporada'
        )


class ListaJugadoresSerializer(serializers.ModelSerializer):

    posicion_principal = PosicionSerializer()

    class Meta:
        model = Jugador
        fields = (
            'id',
            'nombre',
            'apellidos',
            'posicion_principal'
        )

class JugadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jugador
        fields = (
            'id',
            'nombre',
            'apellidos',
            'fecha_nacimiento',
            'altura',
            'posicion_principal',
            'posiciones_secundarias',
            'pie_dominante',
            'equipo'
        )

class EstadisticasJugadorPartidos(serializers.ModelSerializer):

    class Meta:
        model = DatosPartido
        fields = (
            'valoracion_partido',
            'amarillas',
            'goles',
            'asistencias',
            'tiros_puerta',
            'minutos_jugados',
            'plus_minutos_por_lesion'
        )

# class EstadisticasJugadorEntrenamientos(serializers.ModelSerializer):

#     class Meta:
#         model = DatosEntrenamiento
#         fields = (
#             'minutos_jugados',
#             'plus_minutos_por_lesion'
#         )

class EstadisticasFinalesSerializer(serializers.Serializer):

    partidos_jugados = serializers.IntegerField()
    # entrenamientos_asistidos = serializers.IntegerField()
    valoracion_media = serializers.DecimalField(max_digits=5, decimal_places=2)
    amarillas_totales = serializers.IntegerField()
    goles_totales = serializers.IntegerField()
    efectividad_goles = serializers.DecimalField(max_digits=5, decimal_places=2)
    asistencias_totales = serializers.IntegerField()
    probabilidad_lesion = serializers.DecimalField(max_digits=5, decimal_places=2)


class PartidoInformeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partido
        fields = (
            'local',
            'visitante',
            'goles_local',
            'goles_visitante'
        )


class InformeJugadorPartidoSerializer(serializers.ModelSerializer):

    partido = PartidoInformeSerializer()
    posicion_jugada = PosicionSerializer()

    class Meta:
        model = DatosPartido
        fields = (
            'id',
            'valoracion_partido',
            'posicion_jugada',
            'partido'
        )


class CooperJugadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cooper
        fields = (
            'fecha',
            'distancia',
            'vo2max'
        )

class EstadisticasJugadorPorPosicion(serializers.Serializer):

    posicion = serializers.CharField()
    partidos_jugados_en_esta_posicion = serializers.IntegerField()
    valoracion_media = serializers.DecimalField(max_digits=5, decimal_places=2)
    robos_balon = serializers.IntegerField()
    goles_totales = serializers.IntegerField()
    asistencias_totales = serializers.IntegerField()
    amarillas_totales = serializers.IntegerField()
    tiros_puerta_totales = serializers.IntegerField()

class JugadorConEstadisticasSerializer(serializers.ModelSerializer):

    posicion_principal = PosicionSerializer()
    posiciones_secundarias = PosicionSerializer(many=True)
    estadisticas_jugador = serializers.SerializerMethodField()
    estadisticas_por_posicion = serializers.SerializerMethodField()
    informes_partidos = serializers.SerializerMethodField()
    tests_cooper = serializers.SerializerMethodField()

    class Meta:
        model = Jugador
        fields = (
            'id',
            'nombre',
            'apellidos',
            'fecha_nacimiento',
            'altura',
            'posicion_principal',
            'posiciones_secundarias',
            'pie_dominante',
            'estadisticas_jugador',
            'estadisticas_por_posicion',
            'informes_partidos',
            'tests_cooper'
            # informes_entrenamientos
            # faltas_a_entrenamientos
        )

    def calcula_estadisticas(self, datos_partidos):

        total_amarillas = 0
        total_goles = 0
        total_asistencias = 0
        total_tiros_puerta = 0
        total_minutos_jugados = 0
        valoracion_total = 0
        ac = 0

        for informe in datos_partidos:
            if informe['amarillas']:
                total_amarillas = total_amarillas + informe['amarillas']
            

            if informe['goles']:
                total_goles = total_goles + informe['goles']
            

            if informe['asistencias']:
                total_asistencias = total_asistencias + informe['asistencias']
            
            if informe['valoracion_partido']:
                valoracion_total = valoracion_total + float(informe['valoracion_partido'])
    
            if informe['tiros_puerta']:
                total_tiros_puerta = total_tiros_puerta + informe['tiros_puerta']
    
            if informe['minutos_jugados']:
                total_minutos_jugados = total_minutos_jugados + informe['minutos_jugados']

            if informe['plus_minutos_por_lesion']:
                total_minutos_jugados = total_minutos_jugados + informe['plus_minutos_por_lesion']

            ac = ac + 1

        if total_goles > 0:
            efectividad_goles = (total_goles / total_tiros_puerta) * 100
        else:
            efectividad_goles = 0
        
        if valoracion_total > 0:
            valoracion_media = valoracion_total / ac
        else:
            valoracion_media = 0

        partidos_jugados = ac

        return (total_amarillas, total_goles, total_asistencias, efectividad_goles, total_minutos_jugados, valoracion_media, partidos_jugados)

    def get_estadisticas_jugador(self, obj):
        query = DatosPartido.objects.filter(jugador__id=obj.id)
        datos_partido_serializados = EstadisticasJugadorPartidos(query, many=True).data
        # datos_entrenamiento_serializados = EstadisticasJugadorEntrenamiento(query, many=True).data    # Sacar de aquí los minutos para sumárselos a la probabilidad de lesión
        
        total_amarillas, total_goles, total_asistencias, efectividad_goles, total_minutos_jugados, valoracion_media, partidos_jugados = self.calcula_estadisticas(datos_partido_serializados)
        # total_minutos_entrenados, entrenamientos_asistidos = calcula_estadisticas_entrenamientos(datos_entrenamiento_serializados)

        # TODO Probabilidad de lesión
        total_minutos = total_minutos_jugados # + total_minutos_entrenados

        probabilidad_lesion = (total_minutos / 1000) * 10

        estadisticas = ReturnDict((
            ('partidos_jugados', partidos_jugados),
            # ('entrenamientos_asistidos', entrenamientos_asistidos),
            ('valoracion_media', valoracion_media),
            ('amarillas_totales', total_amarillas),
            ('goles_totales', total_goles),
            ('efectividad_goles', efectividad_goles),
            ('asistencias_totales', total_asistencias),
            ('probabilidad_lesion', probabilidad_lesion)
        ), serializer=EstadisticasFinalesSerializer())
        
        return estadisticas

    def get_estadisticas_por_posicion(self, obj):
        query = DatosPartido.objects.datos_jugador_por_posicion(obj.id)
        estadisticas_serializadas = EstadisticasJugadorPorPosicion(query, many=True).data
        return estadisticas_serializadas

    def get_informes_partidos(self, obj):
        query = DatosPartido.objects.filter(jugador__id = obj.id)
        informes_serializados = InformeJugadorPartidoSerializer(query, many=True).data
        return informes_serializados


    def get_tests_cooper(self, obj):
        query = Cooper.objects.filter(jugador__id = obj.id)
        tests_cooper_serializadas = CooperJugadorSerializer(query, many=True).data
        return tests_cooper_serializadas


class EstadisticasFinalesPorPosicionSerializer(serializers.Serializer):

    valoracion_media = serializers.DecimalField(max_digits=5, decimal_places=2)
    amarillas_totales = serializers.IntegerField()
    goles_totales = serializers.IntegerField()
    efectividad_goles = serializers.DecimalField(max_digits=5, decimal_places=2)
    asistencias_totales = serializers.IntegerField()
    minutos_totales_jugados = serializers.IntegerField()


class DatosPorPosicionTodosLosJugadoresSerializer(serializers.Serializer):

    jugador = serializers.CharField()
    partidos_jugados_en_esta_posicion = serializers.IntegerField()
    valoracion_media = serializers.DecimalField(max_digits=5, decimal_places=2)
    robos_balon = serializers.IntegerField()
    goles_totales = serializers.IntegerField()
    asistencias_totales = serializers.IntegerField()
    amarillas_totales = serializers.IntegerField()
    tiros_puerta_totales = serializers.IntegerField()
    efectividad_goles = serializers.DecimalField(max_digits=5, decimal_places=2)


class DatosPosicionSerializer(serializers.Serializer):

    posicion = serializers.CharField()
    estadisticas = DatosPorPosicionTodosLosJugadoresSerializer(many=True)


class SegundoMejorJugadorSerializer(serializers.Serializer):

    jugador = serializers.CharField()
    valoracion_media = serializers.DecimalField(max_digits=5, decimal_places=2)


class OnceIdealSerializer(serializers.Serializer):

    posicion = serializers.CharField()
    jugador = serializers.CharField()
    valoracion_media = serializers.DecimalField(max_digits=5, decimal_places=2)
    segundo_mejor = SegundoMejorJugadorSerializer()


class EstadisticasPorPosicion(serializers.Serializer):
    datos_posicion = DatosPosicionSerializer(many=True)
    once_ideal = OnceIdealSerializer(many=True)