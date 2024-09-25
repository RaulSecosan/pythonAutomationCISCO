class DHCPConfig:
    def __init__(self, ssh_manager, excluded_addresses, pool_name, network, mask, default_router, dns_server):
        """
        Inițializează configurarea DHCP.
        """
        self.ssh_manager = ssh_manager
        self.excluded_addresses = excluded_addresses
        self.pool_name = pool_name
        self.network = network
        self.mask = mask
        self.default_router = default_router
        self.dns_server = dns_server

    def configure_dhcp(self):
        """
        Configurare DHCP pe router.
        """
        commands = [
            'enable',
            'pass',
            'conf t',
            f'ip dhcp pool {self.pool_name}',
            f'network {self.network} {self.mask}',
            f'default-router {self.default_router}',
            f'dns-server {" ".join(self.dns_server)}'
        ]

        # Adaugă comenzile pentru excluderea intervalelor și adreselor individuale
        for address in self.excluded_addresses:
            if '-' in address:
                start_address, end_address = address.split('-')
                commands.append(f'ip dhcp excluded-address {start_address} {end_address}')
            else:
                commands.append(f'ip dhcp excluded-address {address}')

        commands.append('exit')
        commands.append('write')

        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)