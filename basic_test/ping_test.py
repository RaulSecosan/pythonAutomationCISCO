class PingTest:
    def __init__(self, ssh_manager, target_ip=None, source_ip=None):
        self.ssh_manager = ssh_manager
        self.target_ip = target_ip
        self.source_ip = source_ip

    def run_ping_test(self):
        """
        Executes the ping command. If both source and destination IPs are provided,
        it will attempt to run the ping with those IPs. Otherwise, it will run a ping
        to the target IP.
        """
        if self.source_ip and self.target_ip:
            print(f"Running Ping Test from {self.source_ip} to {self.target_ip}...")
            # Ping with both source and target IPs
            ping_command = f'ping {self.target_ip} source {self.source_ip}'
        else:
            print(f"Running Ping Test to {self.target_ip}...")
            # Ping only the target IP
            ping_command = f'ping {self.target_ip}'

        ping_output = self.ssh_manager.send_command(ping_command)

        if "Success" in ping_output or "!" in ping_output:
            print(f"Ping to {self.target_ip} was successful.")
        else:
            print(f"Ping to {self.target_ip} failed.")
