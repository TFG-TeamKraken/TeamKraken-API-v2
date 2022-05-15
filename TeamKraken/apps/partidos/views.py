from django.shortcuts import render

# Create your views here.

# NOTA: Cuando se vaya a crear un DatosPartido para un jugador, comprobar si existe ya uno en la BD con el mismo partido_id y el mismo jugador_id. Si existe, devolver error 