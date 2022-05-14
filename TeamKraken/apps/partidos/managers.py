from django.db import models
from django.db.models import Avg, Sum
from django.db.models.functions import Upper

class DatosPartidoManager(models.Manager):

    def datos_jugador_por_posicion(self, jugador_id):

        return self.filter(jugador__id = jugador_id).values('posicion_jugada__id').annotate(
                        posicion = Upper('posicion_jugada__abreviacion'),
                        valoracion_media = Avg('valoracion_partido'),
                        robos_balon = Sum('robos_balon'),
                        goles_totales = Sum('goles'),
                        asistencias_totales = Sum('asistencias'),
                        amarillas_totales = Sum('amarillas'),
                        tiros_puerta_totales = Sum('tiros_puerta')
                    )

    def datos_por_posicion(self, username, equipo_id):

        queryset = self.filter(jugador__equipo__user__username = username, jugador__equipo__id = equipo_id).values('posicion_jugada__id', 'jugador__id').annotate(
                        posicion = Upper('posicion_jugada__abreviacion'),
                        nombre_jugador = Upper('jugador__nombre'),
                        apellidos_jugador = Upper('jugador__apellidos'),
                        valoracion_media = Avg('valoracion_partido'),
                        robos_balon = Sum('robos_balon'),
                        goles_totales = Sum('goles'),
                        asistencias_totales = Sum('asistencias'),
                        amarillas_totales = Sum('amarillas'),
                        tiros_puerta_totales = Sum('tiros_puerta')
                    )

        queryset_clasificada = [
            {
                'posicion': 'PT',
                'estadisticas' : []
            },
            {
                'posicion': 'CTD',
                'estadisticas' : []
            },
            {
                'posicion': 'CTI',
                'estadisticas' : []
            },
            {
                'posicion': 'LI',
                'estadisticas' : []
            },
            {
                'posicion': 'LD',
                'estadisticas' : []
            },
            {
                'posicion': 'MCD',
                'estadisticas' : []
            },
            {
                'posicion': 'MC',
                'estadisticas' : []
            },
            {
                'posicion': 'II',
                'estadisticas' : []
            },
            {
                'posicion': 'ID',
                'estadisticas' : []
            },
            {
                'posicion': 'MP',
                'estadisticas' : []
            },
            {
                'posicion': 'SP',
                'estadisticas' : []
            },
            {
                'posicion': 'EI',
                'estadisticas' : []
            },
            {
                'posicion': 'ED',
                'estadisticas' : []
            },
            {
                'posicion': 'DC',
                'estadisticas': []
            }
        ]
        
        for result in queryset:

            # Concatenación de nombre y apellidos del jugador
            result['jugador'] = result['nombre_jugador'] + ' ' + result['apellidos_jugador']
            
            # Cálculo de la efectividad en los goles del jugador en la posición correspondiente
            if result['tiros_puerta_totales'] > 0 :
                result['efectividad_goles'] = (result['goles_totales'] / result['tiros_puerta_totales']) * 100
            else:
                result['efectividad_goles'] = 0
            
            # Actualización de la lista clasificada de datos por posición con el objeto actual
            queryset_clasificada[result['posicion_jugada__id'] - 1]['estadisticas'].append(result)

        return queryset_clasificada