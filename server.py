# echo-server.py

import socket
import time

# Connection values
HOST = "172.168.100.188"  # IP address
PORT = 4321  # Port to listen on (non-privileged ports are > 1023)

# message = "Hello from Python"


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
                print(f"\n\nConnected by {addr}\n{data}")
                # conn.send(message.encode())
                split = data.split(",")
                imu = split[2]
                print(f"Temperatura: {imu[0]}{imu[1]}")
                print(f"Conteo de activaciones: {imu[3]}{imu[4]}{imu[5]}")
                print(f"Hombre caído: {imu[11]}")
                print(f"¿Activo?: {imu[12]}")
                print(f"Evacuación: {imu[13]}")
                print(f"Auxilio: {imu[14]}")
                print(f"Recibido: {imu[15]}")
                time.sleep(1)


def main():
    tcp_server()


if __name__ == "__main__":
    main()
