from django.db import models
from django.db.models import Avg, Sum, Count
from django.db.models.functions import Upper

from operator import attrgetter

class DatosPartidoManager(models.Manager):

    def datos_jugador_por_posicion(self, jugador_id):

        return self.filter(jugador__id = jugador_id).values('posicion_jugada__id').annotate(
                        posicion = Upper('posicion_jugada__abreviacion'),
                        partidos_jugados_en_esta_posicion = Count('posicion_jugada__id'), 
                        valoracion_media = Avg('valoracion_partido'),
                        robos_balon = Sum('robos_balon'),
                        goles_totales = Sum('goles'),
                        asistencias_totales = Sum('asistencias'),
                        amarillas_totales = Sum('amarillas'),
                        tiros_puerta_totales = Sum('tiros_puerta')
                    )

    def existe_jugador_en_el_once(self, mejor_jugador, once_ideal):

        for jugador in once_ideal:
            
            if jugador['posicion'] == mejor_jugador['posicion'] and jugador['jugador'] == mejor_jugador['jugador'] and jugador['valoracion_media'] == mejor_jugador['valoracion_media']:
                return True
        
        return False


    def datos_por_posicion(self, username, equipo_id):

        queryset = self.filter(jugador__equipo__user__username = username, jugador__equipo__id = equipo_id).values('posicion_jugada__id', 'jugador__id').annotate(
                        posicion = Upper('posicion_jugada__abreviacion'),
                        partidos_jugados_en_esta_posicion = Count('posicion_jugada__id'), 
                        nombre_jugador = Upper('jugador__nombre'),
                        apellidos_jugador = Upper('jugador__apellidos'),
                        valoracion_media = Avg('valoracion_partido'),
                        robos_balon = Sum('robos_balon'),
                        goles_totales = Sum('goles'),
                        asistencias_totales = Sum('asistencias'),
                        amarillas_totales = Sum('amarillas'),
                        tiros_puerta_totales = Sum('tiros_puerta')
                    ).order_by('-valoracion_media')

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

        once_ideal = [
            {
                'posicion': 'PT',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'CTD',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'CTI',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'LI',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'LD',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'MCD',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'MC',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'II',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'ID',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'MP',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'SP',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'EI',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'ED',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
            {
                'posicion': 'DC',
                'jugador': '',
                'valoracion_media': 0,
                'segundo_mejor': {
                    'jugador': '',
                    'valoracion_media': 0
                }
            },
        ]
        
        for result in queryset:

            # Concatenación de nombre y apellidos del jugador
            result['jugador'] = result['nombre_jugador'] + ' ' + result['apellidos_jugador']
            
            # Cálculo de la efectividad en los goles del jugador en la posición correspondiente
            if result['tiros_puerta_totales'] is not None:

                if result['tiros_puerta_totales'] > 0:
                    result['efectividad_goles'] = (result['goles_totales'] / result['tiros_puerta_totales']) * 100
                else:
                    result['efectividad_goles'] = 0
                
                # Actualización de la lista clasificada de datos por posición con el objeto actual
                queryset_clasificada[result['posicion_jugada__id'] - 1]['estadisticas'].append(result)
        
        index = 0
        
        for datos_posicion in queryset_clasificada:

            mejor_jugador = datos_posicion['estadisticas'][0]

            once_ideal[index]['jugador'] = mejor_jugador['jugador']
            once_ideal[index]['valoracion_media'] = mejor_jugador['valoracion_media']
            
            if len(datos_posicion['estadisticas']) > 1:
                segundo_mejor_jugador = datos_posicion['estadisticas'][1]

                once_ideal[index]['segundo_mejor']['jugador'] = segundo_mejor_jugador['jugador']
                once_ideal[index]['segundo_mejor']['valoracion_media'] = segundo_mejor_jugador['valoracion_media']
            else:
                once_ideal[index]['segundo_mejor']['jugador'] = 'No hay más opciones para esta posición'

            index = index + 1

        estadisticas_por_posicion = [
            {
                'datos_posicion' : queryset_clasificada,
                'once_ideal': once_ideal
            }
        ]
        
        print(estadisticas_por_posicion)
            
        return estadisticas_por_posicion