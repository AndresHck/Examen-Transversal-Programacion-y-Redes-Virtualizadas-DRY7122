# cambiar_hostname.py
# Cambia el hostname del router usando NETCONF.

from ncclient import manager

# --- Datos de conexión ---
ROUTER_IP = "192.168.77.129" # IP actualizada de tu CSR1000v
ROUTER_USER = "cisco"
ROUTER_PASS = "cisco123!"
ROUTER_PORT = 830

# --- Payload de configuración en formato XML ---
# Reemplaza "Rojas-Guinel" con los apellidos de tu grupo
HOSTNAME_CONFIG_XML = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Rojas-Guinel</hostname>
  </native>
</config>
"""

def change_hostname():
    """
    Se conecta al router y cambia su hostname.
    """
    print("--- Cambiando el hostname del router a 'Rojas-Guinel'... ---")
    try:
        with manager.connect(host=ROUTER_IP, port=ROUTER_PORT, username=ROUTER_USER, password=ROUTER_PASS, hostkey_verify=False) as m:

            # Enviamos la configuración
            edit_response = m.edit_config(target='running', config=HOSTNAME_CONFIG_XML)

            # La respuesta debe ser <ok/> si todo salió bien
            print(f"Respuesta del router: {edit_response}")
            print("¡Hostname cambiado exitosamente!")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == '__main__':
    change_hostname()

