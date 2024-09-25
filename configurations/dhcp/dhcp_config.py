class DHCPConfig:
    def __init__(self, ssh_manager, excluded_addresses, pool_name, network, subnet_mask, gateway, dns_servers, lease_days):
        """
        Inițializează configurarea DHCP.
        """
        self.ssh_manager = ssh_manager
        self.excluded_addresses = excluded_addresses
        self.pool_name = pool_name
        self.network = network
        self.subnet_mask = subnet_mask
        self.gateway = gateway
        self.dns_servers = dns_servers

    def configure_dhcp(self):
        """
        Configurare DHCP pe router.
        """
        commands = [
            'enable',
            'pass',
            'conf t',
            f'ip dhcp excluded-address {self.excluded_addresses[0]} {self.excluded_addresses[1]}',
            f'ip dhcp pool {self.pool_name}',
            f'network {self.network} {self.subnet_mask}',
            f'default-router {self.gateway}',
            f'dns-server {" ".join(self.dns_servers)}',
            'exit',
            'do write'
        ]

        for command in commands:
            output = self.ssh_manager.send_command(command)
            print(output)