import socket


def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connection values
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print(f"Host IP: {host_ip}")
    port = 8077  # Port to listen on (non-privileged ports are > 1023)
    socket_address = (host_ip, port)

    # Bind and listen to the connection values
    server_socket.bind(socket_address)
    server_socket.listen()
    print(f"Waiting connection, listening at {socket_address}...")

    # Client connection accept
    conn, addr = server_socket.accept()
    print(f"Connection from: {addr}")
    if conn:
        conn.send("Welcome to the server!".encode())
    conn.close()


def main():
    tcp_server()


if __name__ == "__main__":
    main()
