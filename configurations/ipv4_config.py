# from ssh_connection.ssh_connection import SSHManager

def configure_ipv4(ssh_manager, ip_addresses):
    """
    Configurare adrese IPv4 pe un dispozitiv.
    """
    for ip_info in ip_addresses:
        interface = ip_info['interface']
        ip_address = ip_info['address']
        mask = ip_info['mask']

        # Asignează IP-ul pe interfață
        commands = [
            'enable',
            'pass',
            'conf t',
            f'interface {interface}',
            f'ip address {ip_address} {mask}',
            'no shutdown',
            'exit',
            'do write'
        ]
        for command in commands:
            output = ssh_manager.send_command(command)
            print(output)