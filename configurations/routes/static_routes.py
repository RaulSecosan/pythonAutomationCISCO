def configure_static_routes(ssh_manager, static_routes):
    """
    Configurare rutele statice pe dispozitiv.
    """
    commands = [
        'enable',
        'conf t'
    ]

    # Adaugă fiecare rută statică în lista de comenzi
    for route in static_routes:
        destination = route['destination']
        mask = route['mask']
        next_hop = route['next_hop']
        commands.append(f'ip route {destination} {mask} {next_hop}')

    commands.append('exit')
    commands.append('write')

    # Trimite comenzile la echipament
    for command in commands:
        output = ssh_manager.send_command(command)
        print(output)