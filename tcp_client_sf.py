# echo-client.py

import socket
import time

# Configuration messages
START_MESSAGE = "Starting_Config"
OK_A = "OK_A"
OK_S = "OK_S"
OK_K = "OK_K"
OK_G = "OK_G"
OK_I = "OK_I"
OK_M = "OK_M"
OK_MB = "OK_MB"
OK_C = "OK_C"

# MAC address
MAC = "hola Enrique"

# Connection values
HOST = "172.168.100.177"  # The server's hostname or IP address
PORT = 50007  # The port used by the server


def tcp_client():
    names = []
    values = []

    # Receive parameter, send confirmation function
    def recv_send(command, name, message):
        data_rs = s.recv(1024).decode()
        if data_rs[:2] == command:
            print(f"\nReceived command: {command}")
            parameter = data_rs[2:]
            print(f"\t{name}: {parameter}")
            names.append(name)
            values.append(parameter)

            time.sleep(1)
            s.send(("MAC: " + MAC + "; " + message).encode())

    print("\nSearching for a connection...")
    time.sleep(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(100)
            # Connect to the server
            s.connect((HOST, PORT))
            print(f"\nConnected with server:\nIP: {HOST}\t\tPort: {PORT}")
            # Send MAC address
            print("\nSending data...")
            s.send(MAC.encode())

            # Receive and print START_MESSAGE from the server
            data = s.recv(1024).decode()
            print(f"\nReceived: {data}\n")

            s.close()

        except ConnectionRefusedError:
            retry = ""
            while retry != "y":
                retry = input("\nConnection refused. Type [Y] to retry...").lower()
            if retry == "y":
                print("\nRetrying the connection...")
                tcp_client()


def main():
    for a in range(0, 5):
        tcp_client()


if __name__ == "__main__":
    main()