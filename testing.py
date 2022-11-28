# echo-client.py

import socket
import time

# MAC address
MAC = "9C:50:D1:06:4C:86"

# Connection values
HOST = "172.168.100.95"  # The server's hostname or IP address
PORT = 5432  # The port used by the server


def tcp_client():

    print("\nSearching for a connection...")
    time.sleep(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(30)
        # Connect to the server
        s.connect((HOST, PORT))
        print(f"\nConnected with server:\nIP: {HOST}\t\tPort: {PORT}")

        # Send MAC address
        print("\nSending MAC address...")
        time.sleep(1)
        s.send(MAC.encode())


def main():
    tcp_client()


if __name__ == "__main__":
    main()
