class BPDUGuardConfig:
    def __init__(self, ssh_manager, interfaces):
        self.ssh_manager = ssh_manager
        self.interfaces = interfaces

    def configure_bpdu_guard(self):
        commands = ['enable', 'conf t', 'pass']
        for interface in self.interfaces:
            commands.append(f'interface {interface}')
            commands.append('spanning-tree bpduguard enable')
            commands.append('exit')
        commands.append('do write')

        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)