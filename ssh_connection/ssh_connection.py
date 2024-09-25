import paramiko
from time import sleep
from multiprocessing import Lock
from helpers.decorators import log_decorator

class SSHManager:
    """
    SSHManager handles SSH connections to network devices, implementing a Singleton pattern to
    ensure only one connection per device. It uses Paramiko for connecting and sending commands
    and implements retry logic in case of connection errors. It is thread-safe by using a Lock.
    """
    _instances = {}  # Dictionary to store instances (Singleton pattern)
    _lock = Lock()  # doar un fir de execuție la un moment dat poate modifica variabila

    def __new__(cls, hostname, username, password):
        """
        Singleton: Creates or returns an existing instance for each device (hostname).
        Ensures thread safety by locking during instance creation.
        """
        with cls._lock:
            if hostname not in cls._instances:
                instance = super(SSHManager, cls).__new__(cls)
                cls._instances[hostname] = instance
        return cls._instances[hostname]

    @log_decorator
    def __init__(self, hostname, username, password):
        """
        Initializes the SSH connection if it hasn't already been initialized for this hostname.
        """
        if not hasattr(self, 'initialized'):
            self.hostname = hostname
            self.username = username
            self.password = password
            self.client = None  # SSH client (Paramiko)
            self.shell = None  # SSH shell session
            self.initialized = True  # Marks the instance as initialized

    @log_decorator
    def connect(self):
        """
        Connects to the specified device using Paramiko. If the connection fails, it retries
        up to 3 times. Logs each connection attempt.
        """
        retries = 3
        while retries > 0:
            if self.client is None or not self.client.get_transport().is_active():
                try:
                    print(f"Connecting to {self.hostname}...")
                    self.client = paramiko.SSHClient()
                    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept host keys
                    self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
                    self.shell = self.client.invoke_shell()  # Starts an interactive SSH shell
                    sleep(1)
                    print("Connection established.")
                    break  # Stop retrying if the connection is successful
                except paramiko.SSHException as e:
                    print(f"SSH connection failed: {e}")
                    retries -= 1
                    if retries == 0:
                        raise Exception(f"Could not connect to {self.hostname} after 3 attempts.")

    @log_decorator
    def send_command(self, command):
        """
        Sends a command to the device via the SSH shell. If there's an error sending the command,
        an appropriate error message will be displayed. Handles command execution via the interactive shell.
        """
        if self.shell:
            try:
                self.shell.send(command + '\n')
                sleep(2)
                return self.shell.recv(65535).decode('utf-8')
            except paramiko.SSHException as e:
                print(f"Command execution failed: {e}")
        else:
            print("No active SSH shell. Please connect first.")

    # @log_decorator
    # def execute_command(self, command):
    #     """
    #     Executes a command on the device via SSH without the interactive shell. Uses Paramiko's exec_command.
    #     """
    #     if self.client:
    #         try:
    #             stdin, stdout, stderr = self.client.exec_command(command)
    #             return stdout.read().decode()
    #         except paramiko.SSHException as e:
    #             print(f"Command execution failed: {e}")
    #     else:
    #         print("No active SSH connection. Please connect first.")

    @log_decorator
    def disconnect(self):
        """
        Closes the SSH connection and resets the client.
        """
        if self.client:
            self.client.close()
            self.client = None
            self.shell = None
            print(f"Connection to {self.hostname} closed.")