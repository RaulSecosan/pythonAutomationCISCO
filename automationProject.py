from helpers.yaml_loader import load_yaml_config
from ssh_connection.ssh_connection import SSHManager
from configurations.ipv4_config import configure_ipv4


def main():
    # Încarcă fișierul YAML
    config = load_yaml_config('configurations/devices_config.yaml')

    devices = config['devices']

    for device_name, device_info in devices.items():
        print(f"Configuring {device_name}...")
        ssh_manager = SSHManager(
            hostname=device_info['hostname'],
            username=device_info['username'],
            password=device_info['password']
        )
        ssh_manager.connect()

        # Configurează IP-urile pe dispozitive
        configure_ipv4(ssh_manager, device_info['ip_addresses'])

        ssh_manager.close()


if __name__ == "__main__":
    main()