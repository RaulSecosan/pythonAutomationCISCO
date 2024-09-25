from time import sleep


def configure_rip_v2(ssh_manager):
    """
    Activează RIP v2 și adaugă rețelele bazate pe rutele existente.
    """

    ssh_manager.send_command('enable')
    ssh_manager.send_command('pass')
    ssh_manager.send_command('terminal length 0')  #pentru a afisa toate rutele fara sa apara 'next'
    # Obține rutele curente
    output = ssh_manager.send_command('show ip route')
    sleep(1)

    print(output)

    # Extrage rețelele din `show ip route` (în funcție de ieșirea specifică)
    networks = []
    lines = output.splitlines()
    for line in lines:
        print(line)

        if "C " in line:
            parts = line.split()
            network = parts[1].split('/')[0]
            networks.append(network)
            print(f'This is my {network}')


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
