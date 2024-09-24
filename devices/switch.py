# devices/switch.py

# Import 'NetworkDevice' base class
from devices.base_device import NetworkDevice
# Import 'log_decorator' for logging
from utils.decorators import log_decorator


# Define the 'Switch' class inheriting from 'NetworkDevice'
class Switch(NetworkDevice):
    """
    Class representing a network switch.
    """

    @log_decorator
    def configure_vlans(self, vlans):
        """
        Configure VLANs on the switch.
        """
        # Start with 'configure terminal'
        commands = ['configure terminal']
        # Add VLAN configuration commands
        for vlan_id in vlans:
            commands.extend([
                f'vlan {vlan_id}',
                'exit'
            ])
        # End configuration mode
        commands.append('end')
        # Execute each command
        for cmd in commands:
            self.execute_command(cmd)

    @log_decorator
    def configure_port_security(self, interfaces, max_mac_addresses=1):
        """
        Configure port security on interfaces.
        """
        # Iterate over each interface
        for interface in interfaces:
            # List of commands for port security
            commands = [
                'configure terminal',
                f'interface {interface}',
                'switchport mode access',
                'switchport port-security',
                f'switchport port-security maximum {max_mac_addresses}',
                'switchport port-security violation shutdown',
                'end'
            ]
            # Execute each command
            for cmd in commands:
                self.execute_command(cmd)

    @log_decorator
    def configure_stp_security(self, interfaces):
        """
        Configure STP security features on interfaces.
        """
        # Iterate over each interface
        for interface in interfaces:
            # List of commands for STP security
            commands = [
                'configure terminal',
                f'interface {interface}',
                'spanning-tree portfast',
                'spanning-tree bpduguard enable',
                'end'
            ]
            # Execute each command
            for cmd in commands:
                self.execute_command(cmd)

    @log_decorator
    def verify_connectivity(self, target_ip):
        """
        Verify connectivity to a target IP.
        """
        # Command to ping the target IP
        command = f'ping {target_ip} repeat 5'
        # Execute the ping command and capture the output
        output = self.execute_command(command)
        # Check if the ping was successful
        if 'Success rate is 100 percent' in output:
            # Print success message
            print(f'Connectivity to {target_ip} verified from {self.hostname}')
        else:
            # Print failure message
            print(f'Connectivity to {target_ip} failed from {self.hostname}')
