class PingTest:
    def __init__(self, ssh_manager, target_ip):
        """
        Inițializează clasa pentru a gestiona testul ping.
        """
        self.ssh_manager = ssh_manager
        self.target_ip = target_ip

    def run_ping_test(self):
        """
        Rulează un test ping către IP-ul specificat și verifică rezultatul.
        """
        command = f'ping {self.target_ip}'

        # Trimite comanda ping și primește rezultatul
        output = self.ssh_manager.send_command(command)

        # Verifică succesul ratei de ping din output
        if "Success rate is 100 percent" in output or "!!!!" in output:
            print(f"Ping to {self.target_ip} was successful (100% success).")
        elif "Success rate is" in output:
            print(f"Ping to {self.target_ip} was partially successful.")
        else:
            print(f"Ping to {self.target_ip} failed (no response).")

        # print(output)