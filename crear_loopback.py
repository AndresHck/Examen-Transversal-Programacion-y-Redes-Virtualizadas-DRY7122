# crear_loopback.py
# Crea la interfaz Loopback11 con una IP específica.

from ncclient import manager

# --- Datos de conexión ---
ROUTER_IP = "192.168.77.129" # IP actualizada de tu CSR1000v
ROUTER_USER = "cisco"
ROUTER_PASS = "cisco123!"
ROUTER_PORT = 830

# --- Payload de configuración en formato XML ---
LOOPBACK_CONFIG_XML = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>11</name>
        <description>Interfaz creada con NETCONF para el examen</description>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

def create_loopback():
    """
    Se conecta al router y crea la interfaz Loopback11.
    """
    print("--- Creando la interfaz Loopback11... ---")
    try:
        with manager.connect(host=ROUTER_IP, port=ROUTER_PORT, username=ROUTER_USER, password=ROUTER_PASS, hostkey_verify=False) as m:

            # Enviamos la configuración
            edit_response = m.edit_config(target='running', config=LOOPBACK_CONFIG_XML)

            print(f"Respuesta del router: {edit_response}")
            print("¡Interfaz Loopback11 creada exitosamente!")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == '__main__':
    create_loopback()
