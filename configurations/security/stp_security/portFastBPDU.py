class PortFastBPDUGuardConfig:
    def __init__(self, ssh_manager, interfaces):
        """
        Inițializează managerul pentru configurarea PortFast și BPDUGuard.
        """
        self.ssh_manager = ssh_manager
        self.interfaces = interfaces

    def configure_portfast_bpduguard(self):
        """
        Configurează PortFast și BPDUGuard pe interfețele specificate.
        """
        commands = ['enable', 'pass', 'conf t']

        for interface in self.interfaces:
            commands.append(f'interface {interface}')
            commands.append('spanning-tree portfast')
            commands.append('spanning-tree bpduguard enable')
            commands.append('exit')

        commands.append('do write')

        # Trimite comenzile la echipament
        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)