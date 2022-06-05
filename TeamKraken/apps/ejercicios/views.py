import sys
from django.shortcuts import render
from django.db.models import Q

from time import sleep
from random import randint
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent    # Funciona, aunque VSCode diga que no

from rest_framework.generics import *

from apps.authentication.authentication_mixins import Authentication
from rest_framework.response import Response
from rest_framework import status

from apps.ejercicios.serializers import *
from apps.utils.views import MultipleFieldLookupMixin

sys.setrecursionlimit(10000)

# Create your views here.

class ListaEjercicios(ListAPIView):

    serializer_class = ListaEjerciciosSerializer

    def get_queryset(self):

        queryset = Ejercicio.objects.all()
        username = self.kwargs.get('username')

        if (username is not None):
            queryset = queryset.filter(user__username = username)
            return queryset
        else:
            return Response(
            {
                'error': 'Petición inválida'
            },
            status = status.HTTP_400_BAD_REQUEST
        )

class ListaEjerciciosFiltrada(CreateAPIView):

    serializer_class = QueryEjerciciosSerializer

    def create(self, request, *args, **kwargs):
        
        serializer = QueryEjerciciosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first = serializer.validated_data['first']
        rows = serializer.validated_data['rows']
        last = first + rows
        
        filtros = serializer.validated_data['filters']

        text_filters = (
            ( "nombre__icontains", filtros['nombre']),
            ( "edad_recomendada__icontains", filtros['edad_recomendada']),
            ( "intensidad__icontains",  filtros['intensidad']),
            ( "duracion__icontains", filtros['duracion'])
        )

        list_filters = (
            ( "objetivo_tecnico__id__in", filtros['objetivo_tecnico']),
            ( "objetivo_tactico__id__in", filtros['objetivo_tactico']),
            ( "objetivo_fisico__id__in", filtros['objetivo_fisico']),
            ( "objetivo_psicologico__id__in", filtros['objetivo_psicologico']),
            ( "objetivo_especifico__id__in", filtros['objetivo_especifico'])
        )

        queryset = Ejercicio.objects.all()
        query = None
        for operacion, value in text_filters :

            if value != "":
                if query:
                    query = query & Q( **{ operacion: value} )
                else:
                    query =     Q( **{ operacion: value} )

        for operacion, value in list_filters :

            if len(value) > 0:
                if query:
                    query = query & Q( **{ operacion: value} )
                else:
                    query =     Q( **{ operacion: value} )

        if query:
            queryset = queryset.filter(query).distinct()[first:last]
        else:
            queryset = queryset[first:last]

        ejercicios_filtrados = ListaEjerciciosSerializer(data=queryset, many=True)
        ejercicios_filtrados.is_valid()

        return Response({
            'total_results' : len(ejercicios_filtrados.data),
            'results': ejercicios_filtrados.data
        })


class DetallesEjercicio(MultipleFieldLookupMixin, RetrieveAPIView):
    queryset = Ejercicio.objects.all()
    serializer_class = DetallesEjercicioSerializer
    
    lookup_fields = ['user__username','id']


class CrearEjercicio(CreateAPIView):

    serializer_class = EjercicioSerializer
    

class ActualizarEjercicio(MultipleFieldLookupMixin, RetrieveUpdateAPIView):
    
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer

    lookup_fields = ['user__username', 'id']

    
class EliminarEjercicio(MultipleFieldLookupMixin, DestroyAPIView):

    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer

    lookup_fields = ['user__username', 'id']

#----------------BEAUTIFUL SOUP------------------------
class FetchEjercicios(CreateAPIView):

    serializer_class = ListaNuevosEjerciciosSerializer

    def create(self, request, *args, **kwargs):

        edades_y_num_pages = [
            { 
                'rango': 'edad-menos-de-8-anos',
                'num_pages': 15
            },
            { 
                'rango': 'edad-8-a-11-anos',
                'num_pages': 1
            },
            { 
                'rango': 'edad-11-a-14-anos',
                'num_pages': 8
            },
            { 
                'rango': 'edad-14-a-18-anos',
                'num_pages': 7
            },
            { 
                'rango': 'edad-mas-de-18-anos',
                'num_pages': 1
            }
        ]

        total_ejercicios_created = {
            'edad-menos-de-8-anos' : 0,
            'edad-8-a-11-anos' : 0,
            'edad-11-a-14-anos' : 0,
            'edad-14-a-18-anos' : 0,
            'edad-mas-de-18-anos' : 0
        }

        for elem in edades_y_num_pages:

            print("Fetch for ", elem['rango'], elem['num_pages'])

            fetch_result = self.extraer_ejercicios(elem['rango'], elem['num_pages'])

            serializer = ListaNuevosEjerciciosSerializer(data=fetch_result)
            serializer.is_valid(raise_exception=True)

            ejercicios_created = 0

            for ejercicio in serializer.validated_data['ejercicios']:

                nuevo_ejercicio = Ejercicio.objects.get_or_create(
                    nombre = ejercicio['nombre'],
                    materiales = ejercicio['materiales'],
                    representacion = ejercicio['representacion'],
                    edad_recomendada = ejercicio['edad_recomendada'],
                    dificultad = ejercicio['dificultad'],
                    intensidad = ejercicio['intensidad'],
                    duracion = ejercicio['duracion'],
                    descripcion = ejercicio['descripcion'],
                    consejos = ejercicio['consejos'],
                    user = ejercicio['user'],
                )

                print(nuevo_ejercicio)

                if nuevo_ejercicio[1]:
                    print('Setted objetivos')
                    nuevo_ejercicio[0].objetivo_tecnico.set(ejercicio['objetivo_tecnico'])
                    nuevo_ejercicio[0].objetivo_tactico.set(ejercicio['objetivo_tactico'])
                    nuevo_ejercicio[0].objetivo_fisico.set(ejercicio['objetivo_fisico'])
                    nuevo_ejercicio[0].objetivo_psicologico.set(ejercicio['objetivo_psicologico'])
                    nuevo_ejercicio[0].objetivo_especifico.set(ejercicio['objetivo_especifico'])

                    ejercicios_created = ejercicios_created + 1
            
            total_ejercicios_created[elem['rango']] = ejercicios_created
            print("Ejercicios creados para " + elem['rango'] +  ": " + str(ejercicios_created))

        return Response(total_ejercicios_created)

    def extraer_ejercicios(self, rango_edad, num_pages):

        lista = []

        # Creamos un User Agent falso para evitar las herramientas anti-scraping.
        ua = UserAgent()
        fake_user_agent = ua.random

        # Inicializamos el driver de Selenium, que nos servirá para evitar el formulario de aceptación de las cookies de la página, 
        # además de agregar nuestro User Agent falso.
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument(f'user-agent={fake_user_agent}')
        print(options.arguments)
        driver = webdriver.Chrome('C:/Windows/chromedriver/chromedriver.exe', chrome_options=options)

        index = 1

        while index <= num_pages:

            # Ejecutamos el driver con la página deseada
            driver.get("http://entrenamientosdefutbol.es/" + rango_edad + "/?pagina=" + str(index))

            print("Accediendo a " + "http://entrenamientosdefutbol.es/" + rango_edad + "/?pagina=" + str(index))

            page_source = driver.page_source
            s = BeautifulSoup(page_source,"lxml")
            l = s.find_all("div", class_="title")
            
            for e in l:
                objetivos_especificos = []
                objetivos_fisicos = []
                objetivos_psicologicos = []
                objetivos_tacticos = []
                objetivos_tecnicos = []
                driver.get("http://entrenamientosdefutbol.es/"+e.a['href'])
                page_source = driver.page_source
                ej = BeautifulSoup(page_source,"lxml")

                # Gif del ejercicio

                img_element = ej.find("div", class_="image").find("img")

                gif_ejercicio = "http://entrenamientosdefutbol.es" + img_element['src']

                # Nombre, descripción
                nombre = ej.find("h1").string
                aux = ej.find("h1").find_next_sibling("p")
                parrafos = aux.contents
                descripcion = ""
                i = 0
                for d in parrafos:
                    if i == 0 or i % 2 == 0:
                        descripcion = descripcion + str(d) + ". "
                    i = i + 1
                div_contents = ej.find_all("div", class_="content")

                # Edad, dificultad, intensidad, duración

                parent = aux.parent
                div_datos_ejercicio = parent.find_next_sibling("div")
                contents = div_datos_ejercicio.find_all("p")

                edad_recomendada = contents[0].string.strip()

                dificultad = contents[2].string.strip()

                intensidad = contents[4].string.strip()

                div_duracion = div_datos_ejercicio.find("span").contents
                duracion = div_duracion[3].string + div_duracion[4]

                #MATERIALES
                div_materiales = div_contents[1]
                lista_materiales = div_materiales.find_all("li")
                materiales = ""
                for material in lista_materiales:
                    if len(material.contents) > 1:
                        materiales = materiales + "Dimensiones del campo:" + str(material.contents[1])
                    else:
                        materiales = materiales + str(material.string) + " \n " 

                #CONSEJOS
                div_consejos = div_contents[2]
                lista_consejos = div_consejos.find_all("li")
                consejos = ""
                i = 0
                for consejo in lista_consejos:
                    aux = str(consejo.contents[4])
                    aux2 = aux.replace(": ", "").replace(".", "")
                    if i == (len(lista_consejos) - 1):
                        consejos = consejos + str(aux2)
                    else:
                        consejos = consejos + str(aux2) + " \n "
                    i = i + 1
                
                #OBJETIVOS
                div_objetivos = div_contents[3]
                h4_objetivos = div_objetivos.find_all("h4", class_="panel-title")
                for h4 in h4_objetivos:
                    # sleep(randint(3, 7))    # Sleep para evitar el anti-scarping
                    if h4.string == "Objetivos Específicos":
                        parent = h4.parent
                        vecino = parent.find_next_sibling("div")
                        li_objetivos = vecino.find_all("li")
                        for li in li_objetivos:
                            nombre_objetivo_especifico = li.a.string
                            objetivo_especifico = ObjetivoEspecifico.objects.get_or_create(nombre=nombre_objetivo_especifico)
                            objetivos_especificos.append(objetivo_especifico[0].id)

                    elif h4.string == "Objetivos Físicos":
                        parent = h4.parent
                        vecino = parent.find_next_sibling("div")
                        li_objetivos = vecino.find_all("li")
                        for li in li_objetivos:
                            nombre_objetivo_fisico = li.a.string
                            objetivo_fisico = ObjetivoFisico.objects.get_or_create(nombre=nombre_objetivo_fisico)
                            objetivos_fisicos.append(objetivo_fisico[0].id)

                    elif h4.string == "Objetivos Psicológicos":
                        parent = h4.parent
                        vecino = parent.find_next_sibling("div")
                        li_objetivos = vecino.find_all("li")
                        for li in li_objetivos:
                            nombre_objetivo_psicologico = li.a.string
                            objetivo_psicologico = ObjetivoPsicologico.objects.get_or_create(nombre=nombre_objetivo_psicologico)
                            objetivos_psicologicos.append(objetivo_psicologico[0].id)

                    elif h4.string == "Objetivos Tácticos":
                        parent = h4.parent
                        vecino = parent.find_next_sibling("div")
                        li_objetivos = vecino.find_all("li")
                        for li in li_objetivos:
                            nombre_objetivo_tactico = li.a.string
                            objetivo_tactico = ObjetivoTactico.objects.get_or_create(nombre=nombre_objetivo_tactico)
                            objetivos_tacticos.append(objetivo_tactico[0].id)

                    elif h4.string == "Objetivos Técnicos":
                        parent = h4.parent
                        vecino = parent.find_next_sibling("div")
                        li_objetivos = vecino.find_all("li")
                        for li in li_objetivos:
                            nombre_objetivo_tecnico = li.a.string
                            objetivo_tecnico = ObjetivoTecnico.objects.get_or_create(nombre=nombre_objetivo_tecnico)
                            objetivos_tecnicos.append(objetivo_tecnico[0].id)

                lista.append(
                        {
                            "nombre": nombre,
                            "representacion": gif_ejercicio,
                            "materiales": materiales, 
                            "consejos": consejos, 
                            "descripcion": descripcion,
                            "edad_recomendada": edad_recomendada,
                            "dificultad": dificultad,
                            "intensidad": intensidad,
                            "duracion": duracion,
                            "objetivo_tecnico": objetivos_tecnicos,
                            "objetivo_tactico": objetivos_tacticos, 
                            "objetivo_fisico": objetivos_fisicos,
                            "objetivo_psicologico": objetivos_psicologicos, 
                            "objetivo_especifico": objetivos_especificos,
                            "created_by_user": False,
                            "user": 1
                        }
                    )

            index = index + 1 

            print(len(lista))

        return { "ejercicios" : lista }