# Script para demostrar la conexión a un router usando NETCONF.

from ncclient import manager
import xml.dom.minidom

# --- Datos de conexión al router CSR1000v ---
ROUTER_IP = "192.168.77.129" # IP actualizada de tu CSR1000v
ROUTER_USER = "cisco"
ROUTER_PASS = "cisco123!"
ROUTER_PORT = 830

def connect_and_show_capabilities():
    """
    Se conecta al router vía NETCONF y muestra las capacidades del servidor.
    """
    print(f"--- Intentando conectar a {ROUTER_IP} por el puerto {ROUTER_PORT}... ---")

    try:
        with manager.connect(host=ROUTER_IP,
                             port=ROUTER_PORT,
                             username=ROUTER_USER,
                             password=ROUTER_PASS,
                             hostkey_verify=False, # Deshabilitar en un entorno de laboratorio
                             device_params={'name': 'csr'}) as m:

            print("¡Conexión exitosa!")
            print("\n--- Capacidades del Servidor NETCONF ---")

            # Iteramos sobre las capacidades y las imprimimos
            for capability in m.server_capabilities:
                print(f"- {capability}")

            print("----------------------------------------")

    except Exception as e:
        print(f"Error al conectar o ejecutar: {e}")

if __name__ == '__main__':
    connect_and_show_capabilities()
