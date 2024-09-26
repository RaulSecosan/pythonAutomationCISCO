from basic_test.ping_test import PingTest
from configurations.security.portsecurity.portSecurityConfig import PortSecurityConfig
from configurations.security.shutdown_ports.shutdown_unused_ports import ShutdownUnusedPortsConfig
from configurations.security.stp_security.portFastBPDU import PortFastBPDUGuardConfig
from helpers.yaml_loader import load_yaml_config
from ssh_connection.ssh_connection import SSHManager
from configurations.vlans.vlan_config import Switch
from configurations.hsrp.hsrp_config import HSRPConfig
from configurations.dhcp.dhcp_config import DHCPConfig
from configurations.rstp.rstp_config import RSTPConfig
from configurations.routes.rip_config import configure_rip_v2
from helpers.decorators import read_log_file


class DeviceManager:
    """
    A class to manage network device configurations.

    This class provides methods to configure a variety of network services
    such as DHCP, VLANs, HSRP, RSTP, and also handle security configurations
    like Port Security and STP Security.
    """

    def __init__(self, ssh_manager, device_info, device_name, rip_devices, hsrp_devices):
        """
        Initializes the DeviceManager with specific device information.
        """
        self.ssh_manager = ssh_manager
        self.device_info = device_info
        self.device_name = device_name
        self.rip_devices = rip_devices
        self.hsrp_devices = hsrp_devices

    def display_menu(self):
        """
        Displays the main configuration menu for the device.
        """
        print("1. Run Ping Test")
        print("2. Configure Port Security")
        print("3. Shutdown Unused Ports")
        print("4. Configure VLANs")
        print("5. Configure HSRP")
        print("6. Configure RIP")
        print("7. Configure DHCP")
        print("8. Configure RSTP")
        print("9. Configure Spanning Tree Security")
        print("10. Read log file")
        print("0. Exit")

    def ping_menu(self):
        """
        Displays the ping test menu with options.
        Allows the user to run default ping tests on all devices or
        specify a custom target IP for a specific device.
        """
        while True:
            print("1. Run default Ping Test on all devices")
            print("2. Run Ping Test with custom target IP for specific device")
            print("0. Exit")
            choice = input("Select option: ")
            if choice == "0":
                print("Exiting ping menu...")
                break
            elif choice == "1":
                self.run_ping_test_all_devices()
            elif choice == "2":
                self.run_ping_test_custom_target()
            else:
                print("Invalid option, please try again.")

    def run_ping_test_all_devices(self):
        """
        Runs the ping test for all devices using the default source
        and target IP from the device configuration.
        """
        for device_name, device_info in devices.items():
            if 'ping_test' in device_info:
                source_ip = device_info['hostname']
                target_ip = device_info['ping_test']['target_ip']
                print(f"Running Ping Test from {source_ip} to {target_ip} for {device_name}...")
                ping_test = PingTest(ssh_managers[device_name], target_ip=target_ip)
                ping_test.run_ping_test()
            else:
                print(f"No ping test configured for {device_name}")

    def run_ping_test_custom_target(self):
        """
        Runs the ping test with a custom target IP specified by the user.
        """
        target_ip = input("Enter the target IP: ")
        source_ip = self.device_info['hostname']
        print(f"Running Ping Test from {source_ip} to {target_ip}...")
        ping_test = PingTest(self.ssh_manager, target_ip=target_ip)
        ping_test.run_ping_test()

    def configure_port_security(self):
        """
        Configures port security based on the device configuration.
        Asks the user to specify `max_mac` or uses the default value from
        the YAML configuration.
        """
        if 'port_security' in self.device_info:
            for port_sec in self.device_info['port_security']:
                interface = port_sec['interface']
                # Solicită utilizatorului să introducă max_mac sau să apese Enter pentru valoarea implicită
                max_mac_input = input(f"Enter max MAC addresses for {interface} (press Enter for default {port_sec.get('max_mac', 1)}): ")
                # Dacă utilizatorul apasă doar Enter, se folosește valoarea implicită din config sau 1
                if max_mac_input.strip() == '':
                    max_mac = port_sec.get('max_mac', 1)
                else:
                    max_mac = int(max_mac_input)

                violation_action = port_sec.get('violation_action', 'shutdown')
                mac_addresses = port_sec.get('mac_addresses', [])
                print(f"Configuring Port Security on {interface} for {self.device_name} with max MAC: {max_mac}...")
                port_security = PortSecurityConfig(self.ssh_manager, interface, max_mac, violation_action, mac_addresses)
                port_security.configure_port_security()

    def shutdown_unused_ports(self):
        """
        Shuts down unused ports on a specific device or uses YAML configuration.
        Allows the user to specify a device, or use default devices if none is specified.
        """
        while True:
            device_input = input(
                "Enter device name to shutdown ports (press Enter to use default devices, or 'exit' to return to menu): ")

            if device_input.strip().lower() == 'exit':
                print("Exiting shutdown menu...")
                break  # Ieșim din funcția de shutdown și revenim la meniul principal

            if device_input.strip() == '':
                # Dacă utilizatorul apasă doar Enter, se folosesc toate dispozitivele din YAML
                print("Shutting down unused ports on all devices from YAML...")
                for device_name, device_info in devices.items():
                    if device_info.get('shutdown_unused_ports', False):
                        print(f"Shutting down unused ports on {device_name}...")
                        unused_ports = ShutdownUnusedPortsConfig(ssh_managers[device_name])
                        unused_ports.shutdown_unused_ports()
                    else:
                        print(f"No shutdown port configuration found for {device_name}")
                break  # Ieșim după ce am aplicat shutdown pentru toate dispozitivele
            else:
                # Dacă utilizatorul introduce un nume de dispozitiv, aplicăm configurarea pentru acel dispozitiv specific
                if device_input in devices:
                    print(f"Shutting down unused ports on {device_input} (user specified)...")
                    ssh_manager = ssh_managers[device_input]
                    unused_ports = ShutdownUnusedPortsConfig(ssh_manager)
                    unused_ports.shutdown_unused_ports()
                else:
                    print(f"Device {device_input} not found in the configuration.")

    def configure_vlans(self):
        """
        Configures VLANs on the device based on the VLAN configuration
        in the YAML file.
        """
        if 'vlans' in self.device_info:
            switch = Switch(self.ssh_manager, self.device_info['vlans'])
            switch.configure_vlans()

    def configure_hsrp(self):
        """
        Configures HSRP
        """
        if self.device_name in self.hsrp_devices:
            print(f"Configuring HSRP on {self.device_name}...")
            hsrp_config = self.device_info['hsrp']
            hsrp_manager = HSRPConfig(self.ssh_manager, hsrp_config['interface'], hsrp_config['group'],  hsrp_config['real_ip'], hsrp_config['standby_ip'], hsrp_config['priority'])
            hsrp_manager.configure_hsrp()

    def configure_rip(self):
        """
        Configures RIP
        """
        if self.device_name in self.rip_devices:
            print(f"Configuring RIP on {self.device_name}...")
            configure_rip_v2(self.ssh_manager)

    def configure_dhcp(self):
        """
        Configures DHCP on the device based on the DHCP configuration
        in the YAML file.
        """
        if 'dhcp' in self.device_info:
            dhcp_info = self.device_info['dhcp']
            print(f"Configuring DHCP on {self.device_name}...")
            dhcp_config = DHCPConfig(
                ssh_manager=self.ssh_manager,
                pool_name=dhcp_info['pool_name'],
                network=dhcp_info['network'],
                mask=dhcp_info['mask'],
                default_router=dhcp_info['default_router'],
                dns_server=dhcp_info['dns_server'],
                excluded_addresses=dhcp_info['excluded_addresses']
            )
            dhcp_config.configure_dhcp()

    def configure_rstp(self):
        """
        Configures RSTP
        """
        if self.device_info.get('rstp', False):
            print(f"Configuring RSTP on {self.device_name}...")
            rstp_manager = RSTPConfig(self.ssh_manager)
            rstp_manager.configure_rstp()

    def configure_spanning_tree_security(self):
        """
        Configures Spanning Tree Security (PortFast and BPDU Guard)
        based on the YAML configuration.
        """
        if 'spanning_tree_security' in self.device_info:
            spanning_tree_security_info = self.device_info['spanning_tree_security']
            interfaces = spanning_tree_security_info.get('interfaces', [])
            if interfaces:
                print(f"Configuring Spanning Tree Security on {self.device_name}...")
                spanning_tree_security_manager = PortFastBPDUGuardConfig(self.ssh_manager, interfaces)
                spanning_tree_security_manager.configure_portfast_bpduguard()


def main():
    """
    Main function to load the device configurations, initiate SSH connections,
    and display the configuration menu for each device.
    """
    config = load_yaml_config('configurations/devices_config.yaml')
    global devices
    devices = config['devices']
    rip_devices = config.get('rip_devices', [])
    hsrp_devices = config.get('hsrp_devices', [])

    global ssh_managers
    ssh_managers = {}

    for device_name, device_info in devices.items():
        print(f"Establishing connection to {device_name}...")
        ssh_manager = SSHManager(
            hostname=device_info['hostname'],
            username=device_info['username'],
            password=device_info['password']
        )
        ssh_manager.connect()
        ssh_managers[device_name] = ssh_manager

    while True:
        print("\n--- Main Configuration Menu ---")
        print("1. Run Ping Test")
        print("2. Configure Port Security")
        print("3. Shutdown Unused Ports")
        print("4. Configure VLANs")
        print("5. Configure HSRP")
        print("6. Configure RIP")
        print("7. Configure DHCP")
        print("8. Configure RSTP")
        print("9. Configure Spanning Tree Security")
        print("10. Read log file")
        print("0. Exit")

        choice = input("Select option: ")

        if choice == "0":
            print("Exiting...")
            for ssh_manager in ssh_managers.values():
                ssh_manager.disconnect()
            break

        for device_name, device_info in devices.items():
            menu = DeviceManager(ssh_managers[device_name], device_info, device_name, rip_devices, hsrp_devices)

            if choice == "1":
                menu.ping_menu()
            elif choice == "2":
                menu.configure_port_security()
            elif choice == "3":
                menu.shutdown_unused_ports()
            elif choice == "4":
                menu.configure_vlans()
            elif choice == "5":
                menu.configure_hsrp()
            elif choice == "6":
                menu.configure_rip()
            elif choice == "7":
                menu.configure_dhcp()
            elif choice == "8":
                menu.configure_rstp()
            elif choice == "9":
                menu.configure_spanning_tree_security()
            elif choice == "10":
                read_log_file()
            else:
                print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
