# Script para calcular rutas usando la API de GraphHopper.

import requests
import urllib.parse

# Clave de API para GraphHopper. Para un proyecto real, es mejor guardarla de forma segura.
API_KEY = "b73dedb9-ff8d-4237-91a1-c15ac5d88f86"

def obtener_coordenadas(ubicacion, api_key):
    """
    Convierte el nombre de una ubicación en coordenadas (latitud, longitud)
    usando la API de Geocoding de GraphHopper.
    """
    # URL base para la API de geocodificación
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    
    # Construimos la URL completa con los parámetros necesarios
    url = geocode_url + urllib.parse.urlencode({
        "q": ubicacion,
        "limit": "1",
        "key": api_key,
        "locale": "es"  # Especificamos el idioma español
    })

    try:
        # Hacemos la solicitud a la API
        respuesta = requests.get(url)
        # Si la solicitud no fue exitosa, lanzará un error
        respuesta.raise_for_status()
        
        json_data = respuesta.json()

        # Verificamos que la respuesta contenga resultados
        if json_data["hits"]:
            lat = json_data["hits"][0]["point"]["lat"]
            lng = json_data["hits"][0]["point"]["lng"]
            nombre = json_data["hits"][0]["name"]
            pais = json_data["hits"][0].get("country", "")
            ciudad = json_data["hits"][0].get("city", nombre)
            
            nombre_completo = f"{ciudad}, {pais}" if pais else ciudad
            print(f"Ubicación encontrada: {nombre_completo}")
            return lat, lng, nombre_completo
        else:
            print(f"Error: No se pudo encontrar la ubicación '{ubicacion}'.")
            return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error de red o de API: {e}")
        return None, None, None

def main():
    """
    Función principal del programa.
    """
    print("--- Calculadora de Rutas con GraphHopper ---")
    
    # Demostración inicial entre una ciudad de Chile y una de Argentina
    print("\n--- Demostración: Ruta entre Santiago (Chile) y Mendoza (Argentina) ---")
    calcular_ruta("Santiago, Chile", "Mendoza, Argentina", "car", API_KEY)
    print("--------------------------------------------------------------------")


    while True:
        print("\nPerfiles de vehículos disponibles: car (coche), bike (bicicleta), foot (a pie)")
        vehiculo = input("Introduce un perfil de vehículo (o 's' para salir): ").lower()
        if vehiculo == 's':
            break

        if vehiculo not in ["car", "bike", "foot"]:
            print("Perfil no válido. Usando 'car' por defecto.")
            vehiculo = "car"

        origen_input = input("Introduce la Ciudad de Origen (o 's' para salir): ")
        if origen_input.lower() == 's':
            break

        destino_input = input("Introduce la Ciudad de Destino (o 's' para salir): ")
        if destino_input.lower() == 's':
            break
            
        calcular_ruta(origen_input, destino_input, vehiculo, API_KEY)

    print("\n¡Gracias por usar la calculadora de rutas!")

def calcular_ruta(origen_str, destino_str, vehiculo, api_key):
    """
    Calcula y muestra la información de la ruta entre un origen y un destino.
    """
    # Obtenemos las coordenadas para el origen y el destino
    lat_origen, lon_origen, nombre_origen = obtener_coordenadas(origen_str, api_key)
    if not lat_origen:
        return # Salimos si no se encontró el origen

    lat_destino, lon_destino, nombre_destino = obtener_coordenadas(destino_str, api_key)
    if not lat_destino:
        return # Salimos si no se encontró el destino

    # URL base para la API de enrutamiento
    route_url = "https://graphhopper.com/api/1/route?"
    
    # Construimos la URL de la ruta
    op = f"&point={lat_origen},{lon_origen}"
    dp = f"&point={lat_destino},{lon_destino}"
    
    paths_url = route_url + urllib.parse.urlencode({
        "key": api_key,
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true", # Para obtener la narrativa
        "calc_points": "false" # No necesitamos los puntos del mapa
    }) + op + dp

    try:
        print("\nCalculando ruta...")
        paths_response = requests.get(paths_url)
        paths_response.raise_for_status()
        paths_data = paths_response.json()

        if "paths" in paths_data:
            print("\n--- ¡Ruta Encontrada! ---")
            print(f"Desde: {nombre_origen}")
            print(f"Hasta: {nombre_destino}")
            print("--------------------------")

            # Extraemos distancia y tiempo
            distancia_km = paths_data["paths"][0]["distance"] / 1000
            distancia_millas = distancia_km / 1.60934
            tiempo_ms = paths_data["paths"][0]["time"]
            
            # Convertimos el tiempo a formato HH:MM:SS
            segundos = int((tiempo_ms / 1000) % 60)
            minutos = int((tiempo_ms / (1000 * 60)) % 60)
            horas = int((tiempo_ms / (1000 * 60 * 60)))

            print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
            print(f"Duración del viaje: {horas:02d}h {minutos:02d}m {segundos:02d}s")
            
            # Imprimimos la narrativa del viaje, si está disponible
            if "instructions" in paths_data["paths"][0]:
                print("\n--- Narrativa del Viaje ---")
                for instruccion in paths_data["paths"][0]["instructions"]:
                    dist_inst_km = instruccion['distance'] / 1000
                    print(f"- {instruccion['text']} ({dist_inst_km:.2f} km)")
                print("---------------------------")
            else:
                print("\nNarrativa del viaje no disponible para esta ruta.")

        else:
            print(f"Error al calcular la ruta: {paths_data.get('message', 'Error desconocido')}")

    except requests.exceptions.RequestException as e:
        print(f"Error de red o de API al obtener la ruta: {e}")

# Punto de entrada del script
if __name__ == "__main__":
    main()
