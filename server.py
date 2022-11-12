# echo-server.py

import socket
import time

# Connection values
HOST = "172.168.100.188"  # IP address
PORT = 4321  # Port to listen on (non-privileged ports are > 1023)


def tcp_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind and listen to the connection values
        s.bind((HOST, PORT))
        while True:
            s.listen()
            # print(f"Waiting connection on IP {HOST} with port {PORT}...")

            # Client connection accept
            conn, addr = s.accept()
            with conn:

                data = conn.recv(1024).decode()
                print(f"\nConnected by {addr}{data}")


def main():
    tcp_server()


if __name__ == "__main__":
    main()