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
MAC = "9C:50:D1:06:4C:86"

# Connection values
HOST = "198.51.100.3"  # The server's hostname or IP address
PORT = 27708  # The port used by the server


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
            s.settimeout(10)
            # Connect to the server
            s.connect((HOST, PORT))
            print(f"\nConnected with server:\nIP: {HOST}\t\tPort: {PORT}")

            # Send MAC address
            print("\nSending MAC address...")
            time.sleep(1)
            s.send(MAC.encode())

            # Receive and print START_MESSAGE from the server
            data = s.recv(1024).decode()
            if data == "Starting_Config":
                print(f"\nReceived: {data}\nSending {OK_A} message confirmation.")
                time.sleep(1)

                # Send START_MESSAGE confirmation to the server
                s.send(("MAC: " + MAC + "; " + OK_A).encode())

                # Receive SSID from the server and send confirmation
                recv_send("-S", "SSID", OK_S)

                # Receive Password from the server and send confirmation
                recv_send("-K", "Password", OK_K)

                # Receive IP_Server from the server and send confirmation
                recv_send("-I", "IP server", OK_I)

                # Receive Gate from the server and send confirmation
                recv_send("-G", "Gate", OK_G)

                # Receive Mask from the server and send confirmation
                recv_send("-M", "Mask", OK_M)

                # Receive IP_Client from the server and send confirmation
                recv_send("-C", "IP Client", OK_C)

                data = s.recv(1024).decode()
                if data[:2] == "-E":
                    print("\nReceived command: -E\n\nConfiguration succeed with values:")
                    n = 0
                    for a in names:
                        print(f"\t- {a}: {values[n]}")
                        n += 1
                    print("\nModule restart initiated.")
        except ConnectionRefusedError:
            retry = ""
            while retry != "y":
                retry = input("\nConnection refused. Type [Y] to retry...").lower()
            if retry == "y":
                print("\nRetrying the connection...")
                tcp_client()


def main():
    tcp_client()


if __name__ == "__main__":
    main()
