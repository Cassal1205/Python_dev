# echo-server.py

import socket
import time

# Configuration messages
START_MESSAGE = "Starting_Config"

# Configuration commands
ssid_c = "-S"
key_c = "-K"
ip_server_c = "-I"
gate_c = "-G"
mask_c = "-M"
ip_client_c = "-C"

# Configuration values
SSID = "SF-HARDWARE"
PASSWORD = "Lasec123."
IP_server = "10.86.10.1"
GATE = "121.121.121.121"
MASK = "131.131.131.131"
IP_client = "192.168.0.1"

# Connection values
HOST = "172.168.100.91"  # IP address
PORT = 8077  # Port to listen on (non-privileged ports are > 1023)


def tcp_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Bind and listen to the connection values
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting connection...")

        # Client connection accept
        conn, addr = s.accept()
        with conn:

            # Print connected client values
            print(f"\nConnected by {addr}")
            time.sleep(1)

            # Receive and print MAC address
            data = conn.recv(1024).decode()
            mac = data
            print(f"\nReceived: {mac}")
            print(f"Sending {START_MESSAGE} message...")
            time.sleep(1)

            # Send START_MESSAGE to the client
            conn.send(START_MESSAGE.encode())

            # Receive START_MESSAGE confirmation and send SSID
            recv_send(conn, "SSID", mac, ssid_c, SSID)

            # Receive SSID confirmation and send Password
            recv_send(conn, "Password", mac, key_c, PASSWORD)

            # Receive Password confirmation and send IP server
            recv_send(conn, "IP server", mac, ip_server_c, IP_server)

            # Receive IP confirmation and send Gate
            recv_send(conn, "Gate", mac, gate_c, GATE)

            # Receive Gate confirmation and send Mask
            recv_send(conn, "Mask", mac, mask_c, MASK)

            # Receive Mask confirmation and send IP client
            recv_send(conn, "IP client", mac, ip_client_c, IP_client)


# Receive confirmation, send parameter function
def recv_send(conn, name, mac, command, parameter):
    # Receive confirmation
    data = conn.recv(1024).decode()
    print(f"\nReceived: {data}")
    print(f"Sending {name}...")
    data_split = data.split("; ")
    message = data_split[1]
    time.sleep(1)

    # Send parameter
    if data == ("MAC: " + mac + "; " + message):
        conn.send((command + parameter).encode())


def main():
    tcp_server()


if __name__ == "__main__":
    main()
