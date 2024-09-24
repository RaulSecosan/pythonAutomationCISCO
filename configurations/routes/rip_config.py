def configure_rip_v2(ssh_manager):
    """
    Activează RIP v2 și adaugă rețelele bazate pe rutele existente.
    """

    ssh_manager.send_command('enable')
    ssh_manager.send_command('pass')
    # Obține rutele curente
    output = ssh_manager.send_command('show ip route')
    output += ssh_manager.send_command(' ')

    print(output)

    # Extrage rețelele din `show ip route` (în funcție de ieșirea specifică)
    networks = []
    for line in output.splitlines():
        # if "C " in line or "L " in line:  # C = connected, L = local
        if "C "  in line:
            parts = line.split()
            network = parts[1].split('/')[0]
            networks.append(network)

    # Activează RIP v2 și adaugă rețelele
    commands = [
        'conf t',
        'router rip',
        'version 2',
        'no auto-summary'
    ]

    for network in networks:
        commands.append(f'network {network}')

    commands.append('exit')
    commands.append('do write')

    # Execută comenzile pe router
    for command in commands:
        output = ssh_manager.send_command(command)
        print(output)