class PortSecurityConfig:
    def __init__(self, ssh_manager, interface, max_mac=50, violation_action='shutdown', mac_addresses=None):
        """
        Inițializează configurarea Port Security.
        """
        self.ssh_manager = ssh_manager
        self.interface = interface
        self.max_mac = max_mac
        self.violation_action = violation_action
        self.mac_addresses = mac_addresses or []

    def configure_port_security(self):
        """
        Configurează Port Security pe interfață.
        """
        commands = [
            'enable',
            'pass',
            'conf t',
            f'interface {self.interface}',
            'switchport mode access',
            'switchport port-security',
            f'switchport port-security maximum {self.max_mac}',
            f'switchport port-security violation {self.violation_action}',
        ]

        # Adaugă MAC-uri statice dacă există
        for mac in self.mac_addresses:
            commands.append(f'switchport port-security mac-address {mac}')

        commands.append('exit')
        commands.append('do write')

        # Trimite comenzile la dispozitiv
        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)