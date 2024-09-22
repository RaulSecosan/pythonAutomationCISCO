import paramiko
from time import sleep

class SSHManager:
    def __init__(self, hostname, username, password):
        """Inițializează conexiunea SSH și setează sesiunea."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell = None

    def connect(self):
        """Se conectează la dispozitivul specificat."""
        try:
            print(f"Connecting to {self.hostname}...")
            self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
            self.shell = self.client.invoke_shell()
            sleep(1)
            print("Connection established.")
        except paramiko.SSHException as e:
            print(f"SSH connection failed: {e}")

    def send_command(self, command):
        """Trimite comenzi către echipament."""
        if self.shell:
            self.shell.send(command + '\n')
            sleep(2)
            return self.shell.recv(65535).decode('utf-8')
        else:
            print("No active SSH shell. Please connect first.")

    def close(self):
        """Închide conexiunea SSH."""
        self.client.close()
        print("Connection closed.")
