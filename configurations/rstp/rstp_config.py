class RSTPConfig:
    """
    Inițializează RSTPConfig cu un SSH manager pentru a trimite comenzi.
    """
    def __init__(self, ssh_manager):
        self.ssh_manager = ssh_manager


    def configure_rstp(self):
        print("Configuring RSTP...")
        commands = [
            'enable',
            'pass',
            'conf t',
            'spanning-tree mode rapid-pvst',
            'exit',
            'write'
        ]

        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)