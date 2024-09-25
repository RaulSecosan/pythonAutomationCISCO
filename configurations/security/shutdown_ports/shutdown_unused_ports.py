class ShutdownUnusedPortsConfig:
    def __init__(self, ssh_manager):
        self.ssh_manager = ssh_manager

    def shutdown_unused_ports(self):
        """
        Detectează porturile neutilizate și aplică comanda 'shutdown' automat.
        """
        print("Detecting unused ports...")

        # Trimite comanda pentru a obține lista de porturi și statusul lor
        output = self.ssh_manager.send_command('show ip interface brief')
        print(output)

        # Parsează ieșirea pentru a detecta porturile care nu sunt asignate (status administratively down)
        commands = ['enable','pass', 'conf t']

        for line in output.splitlines():
            if 'down' in line and 'administratively down' not in line:
            # if 'unassigned' in line and 'administratively down' not in line:
                # Extrage numele interfeței din linie
                parts = line.split()
                interface = parts[0]
                commands.append(f'interface {interface}')
                commands.append('shutdown')
                print(f"Shutting down {interface}...")

        commands.append('exit')
        commands.append('write')

        # Trimite comenzile la switch pentru a da shutdown pe porturile neutilizate
        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)