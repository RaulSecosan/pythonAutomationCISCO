# def configure_static_routes(ssh_manager, static_routes):
#     """
#     Configurare rutele statice pe dispozitiv.
#     """
#     commands = [
#         'enable',
#         'conf t'
#     ]
#
#     # Adaugă fiecare rută statică în lista de comenzi
#     for route in static_routes:
#         destination = route['destination']
#         mask = route['mask']
#         next_hop = route['next_hop']
#         commands.append(f'ip route {destination} {mask} {next_hop}')
#
#     commands.append('exit')
#     commands.append('write')
#
# # ------
# #     def configure_route_on_isp1():
# #         # Conectează-te la R1 de pe NetworkAutomation-1
# #         r1_ssh = SSHManager(hostname="192.168.1.1", username="R1", password="cisco")
# #         r1_ssh.connect()
# #
# #         # Deschide SSH de pe R1 către ISP1
# #         print("Opening SSH from R1 to ISP1...")
# #         ssh_to_isp1 = r1_ssh.send_command("ssh -l ISP1 10.10.20.4")
# #
# #         if "password:" in ssh_to_isp1:
# #             r1_ssh.send_command("cisco")
# #
# #         # Configurează ruta statică pe ISP1
# #         print("Configuring static route on ISP1...")
# #         r1_ssh.send_command("enable")
# #         r1_ssh.send_command("conf t")
# #         r1_ssh.send_command("ip route 192.168.1.0 255.255.255.0 10.10.20.1")
# #
# #         print("Static route configured on ISP1.")
# #
# #         # Închide conexiunea
# #         r1_ssh.close()
#
# # ---------
#     # Trimite comenzile la echipament
#     for command in commands:
#         output = ssh_manager.send_command(command)
#         print(output)