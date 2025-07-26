
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def obtener_coordenadas(direccion_completa):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": direccion_completa,
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print("Error en geocodificación:", data["status"])
            return None, None
    except Exception as e:
        print("Error al obtener coordenadas:", e)
        return None, None

def buscar_restaurantes_cercanos(lat, lng, radio=1500):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radio,
        "type": "restaurant",
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] == "OK":
            return data["results"]
        else:
            print("Error al buscar restaurantes:", data["status"])
            return []
    except Exception as e:
        print("Error al buscar restaurantes:", e)
        return []
