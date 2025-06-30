# Este script solicita un número de VLAN y determina su rango.

def verificar_rango_vlan(numero_vlan):
    """
    Verifica si una VLAN está en el rango normal o extendido.
    """
    if 1 <= numero_vlan <= 1005:
        return "Rango Normal"
    elif 1006 <= numero_vlan <= 4094:
        return "Rango Extendido"
    else:
        return "Número de VLAN fuera de rango (válido: 1-4094)"

# Bucle principal para que el programa siga corriendo hasta que el usuario decida salir
while True:
    try:
        # Solicitamos la entrada del usuario
        entrada = input("Introduce el número de VLAN (o 'salir' para terminar): ")

        # Si el usuario quiere salir, rompemos el bucle
        if entrada.lower() == 'salir':
            print("Saliendo del programa.")
            break

        # Convertimos la entrada a un número entero
        vlan_id = int(entrada)
        
        # Llamamos a la función para obtener el resultado
        resultado = verificar_rango_vlan(vlan_id)
        
        # Imprimimos el resultado
        print(f"La VLAN {vlan_id} pertenece al: {resultado}")

    except ValueError:
        # Manejo de error si el usuario no introduce un número
        print("Error: Por favor, introduce un número válido.")
    
    print("-" * 20) # Separador para mayor claridad
