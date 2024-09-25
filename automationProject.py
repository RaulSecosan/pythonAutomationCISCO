from helpers.yaml_loader import load_yaml_config
from ssh_connection.ssh_connection import SSHManager
# from configurations.ipv4_config import configure_ipv4
# from configurations.routes.static_routes import configure_static_routes
from configurations.routes.rip_config import configure_rip_v2
from configurations.vlans.vlan_config import Switch
from configurations.dhcp.dhcp_config import DHCPConfig
def main():
    # Încarcă fișierul YAML
    config = load_yaml_config('configurations/devices_config.yaml')

    devices = config['devices']
    rip_devices = config.get('rip_devices', [])
    hsrp_devices = config.get('hsrp_devices', [])

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

        # if 'ip_addresses' in device_info:
        #     configure_ipv4(ssh_manager, device_info['ip_addresses'])
        #
        # # Configurează rutele statice pe dispozitiv, dacă sunt definite
        # if 'static_routes' in device_info:
        #     configure_static_routes(ssh_manager, device_info['static_routes'])
########

        # # Configurează HSRP pe dispozitivele care au nevoie
        # if device_name in hsrp_devices:
        #     print(f"Configuring HSRP on {device_name}...")
        #     hsrp_config = device_info['hsrp']
        #     hsrp_manager = HSRPConfig(
        #         ssh_manager,
        #         hsrp_config['interface'],
        #         hsrp_config['real_ip'],
        #         hsrp_config['standby_ip'],
        #         hsrp_config['priority']
        #     )
        #     hsrp_manager.configure_hsrp()

        # Configurează RIP pe dispozitivele care au nevoie
        if device_name in rip_devices:
            print(f"Configuring RIP on {device_name}...")
            configure_rip_v2(ssh_manager)

        # # Creează VLAN-urile pe switch
        # if 'vlans' in device_info:
        #     switch = Switch(ssh_manager, device_info['vlans'])
        #     switch.configure_vlans()

        # if 'dhcp' in device_info:
        #     print(f"Configuring DHCP on {device_name}...")
        #     dhcp_config = DHCPConfig(ssh_manager, device_info['dhcp'])
        #     dhcp_config.configure_dhcp()

        ssh_manager.close()


if __name__ == "__main__":
    main()