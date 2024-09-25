class Switch:
    def __init__(self, ssh_manager, vlans):
        """
        Inițializează switch-ul și lista de VLAN-uri.
        """
        self.ssh_manager = ssh_manager
        self.vlans = vlans

    def configure_vlans(self):
        """
        Creează VLAN-uri pe switch.
        """
        commands = ['enable', 'pass','conf t']
        for vlan in self.vlans:
            commands.append(f'vlan {vlan}')
            commands.append(f'name VLAN_{vlan}')

        commands.append('exit')
        commands.append('do write')
        commands.append('do write')

        # Trimite comenzile la switch
        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)