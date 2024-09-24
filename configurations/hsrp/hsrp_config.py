class HSRPConfig:
    def __init__(self, ssh_manager, interface, real_ip, standby_ip, priority):
        """
        Inițializează configurarea HSRP.
        """
        self.ssh_manager = ssh_manager
        self.interface = interface
        self.real_ip = real_ip
        self.standby_ip = standby_ip
        self.priority = priority

    def configure_hsrp(self):
        """
        Configurare HSRP pe un dispozitiv.
        """
        commands = [
            'enable',
            'pass',
            'conf t',
            f'interface {self.interface}',
            # f'ip address {self.real_ip} 255.255.255.0',
            f'standby 1 ip {self.standby_ip}',
            f'standby 1 priority {self.priority}',
            'standby 1 preempt',
            'exit',
            'do write'
        ]

        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)