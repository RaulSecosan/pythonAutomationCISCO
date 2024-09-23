from helpers.yaml_loader import load_yaml_config
from ssh_connection.ssh_connection import SSHManager
from configurations.ipv4_config import configure_ipv4
from configurations.routes.static_routes import configure_static_routes


def main():
    # Încarcă fișierul YAML
    config = load_yaml_config('configurations/devices_config.yaml')

    devices = config['devices']

    # Parcurge fiecare dispozitiv și aplică configurația
    for device_name, device_info in devices.items():
        print(f"Configuring {device_name}...")

        # Inițializează managerul SSH pentru dispozitivul curent
        ssh_manager = SSHManager(
            hostname=device_info['hostname'],
            username=device_info['username'],
            password=device_info['password']
        )
        # Conectare SSH
        ssh_manager.connect()

        # Configurează IP-urile pe dispozitive
        if 'ip_addresses' in device_info:
            configure_ipv4(ssh_manager, device_info['ip_addresses'])

        # Configurează rutele statice pe dispozitiv, dacă sunt definite
        if 'static_routes' in device_info:
            configure_static_routes(ssh_manager, device_info['static_routes'])


        ssh_manager.close()


if __name__ == "__main__":
    main()