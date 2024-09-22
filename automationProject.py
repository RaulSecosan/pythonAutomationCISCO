# Main function to use SSHManager
from ssh_connection.ssh_connection import SSHManager


def main():
    # Declara un SSH manager pentru conexiune
    ssh_manager = SSHManager(hostname="192.168.1.1", username="R1", password="cisco")

    # Conexiunea la echipament
    ssh_manager.connect()

    # Trimite comenzi de configurare
    ssh_manager.send_command("enable\n")
    ssh_manager.send_command("pass\n")
    response = ssh_manager.send_command("show ip int brief\n")

    # Afisare raspuns
    print(response)


    # Închide conexiunea
    ssh_manager.close()


if __name__ == "__main__":
    main()