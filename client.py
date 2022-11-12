# echo-client.py

import socket
import time

# Connection values
HOST = "172.168.100.106"  # The server's hostname or IP address
PORT = 4321  # The port used by the server


def tcp_client():
    print("--- Client socket created ---")
    print("Searching for a connection...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Connect to the server
            s.connect((HOST, PORT))
            print(f"\nConnected with server:\nIP: {HOST}\t\tPort: {PORT}\n")

            message = input("Ingresa el mensaje: ")
            # Send data
            print("Sending data...")
            s.send(message.encode())

            data = (s.recv(65507).decode())

            print(f"Datos recibidos: {data}")

        except ConnectionRefusedError:
            retry = ""
            while retry != "y":
                retry = input("\nConnection refused. Type [Y] to retry...").lower()
            if retry == "y":
                print("\nRetrying the connection...")
                tcp_client()
        s.close()
        print("--- Client socket closed ---")


def main():
    tcp_client()


if __name__ == "__main__":
    main()