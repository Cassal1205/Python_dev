# Import files
import re
import socket
import time
from requests import get


# ----------------------------------------  Constants   ---------------------------------------- #

# Default configuration values
SSID = "SF-HARDWARE"
PASSWORD = "Lasec123."
IP_SERVER = "10.86.10.1"
GATE = "121.121.121.121"
MASK = "131.131.131.131"
IP_CLIENT = "192.168.0.1"

# Configuration messages
START_MESSAGE = "Starting_Config"


# ----------------------------------------  Tuples   ---------------------------------------- #

# Input user filter tuples
SHOW = ("mostrar", "show")
MOD = ("modificar", "mod")
TCP = ("iniciar", "tcp")
EXIT = ("salir", "exit")
BACK = ("atras", "back", "b")
PASS = ("contraseña", "pass", "key", "p", "k")
SERVER = ("ip server", "server")
CLIENT = ("ip client", "client")
IP = ("ip", "i")
YES = ("SI", "S")
NO = ("NO", "N")


# ----------------------------------------  Dictionaries   ---------------------------------------- #

# Parameters dictionary
parameters = dict(ssid=SSID,
                  password=PASSWORD,
                  ip_server=IP_SERVER,
                  gate=GATE,
                  mask=MASK,
                  ip_client=IP_CLIENT)

# Configuration commands dictionary
commands = dict(ssid_c="-S",
                key_c="-K",
                ip_server_c="-I",
                gate_c="-G",
                mask_c="-M",
                ip_client_c="-C",
                succeed_c="-E")

# TCP configuration state dictionary
tcp_conf = dict(Finished=False)

# Empty dictionaries
modified = {}
default = {}


# ----------------------------------------  Functions   ---------------------------------------- #

# Welcome function
def welcome():
    print("\n\t -- Smart Lamp 2v1 --\n\nValores por defecto:")
    list_dictionary(parameters)
    dict_creator()


# Main question function
def ask_to_user():
    return input(f"\n\n\t\t-- INICIO --\n"
                 f"Escribe:\n"
                 f"\t- '{SHOW[0]}/{SHOW[1]}' para mostrar los valores actuales.\n"
                 f"\t- '{MOD[0]}/{MOD[1]}' para modificar algún parámetro.\n"
                 f"\t- '{TCP[0]}/{TCP[1]}' para iniciar el servidor TCP.\n"
                 f"\t- '{EXIT[0]}/{EXIT[1]}' para salir del programa.\n"
                 "\nRespuesta: ")


# Function used several times to list the parameters
def list_dictionary(dictionary):
    for x, y in dictionary.items():
        print(f"\t- {x.upper()}: {y}")


# Function fill/clear the modified/default dictionaries
def dict_creator():
    # Clear all the modified/default values from the dictionaries
    modified.clear()
    default.clear()

    # Function to verify if a value has been modified
    def check_values(p, d):
        if parameters[p] == d:
            default[p] = d
        else:
            modified[p] = parameters[p]

    # Verify SSID
    check_values("ssid", SSID)

    # Verify Password
    check_values("password", PASSWORD)

    # Verify IP_server
    check_values("ip_server", IP_SERVER)

    # Verify Gate
    check_values("gate", GATE)

    # Verify Mask
    check_values("mask", MASK)

    # Verify IP_client
    check_values("ip_client", IP_CLIENT)


# Function to see the parameters and it's current value
def show_values():
    print("\n\n\t\t-- MOSTRAR --")
    # Use the dict creator function
    dict_creator()

    def print_values(dictionary, m1, m2):
        if len(dictionary) >= 1:
            print(f"\n{m1}:")
            list_dictionary(dictionary)
        else:
            print(f"\n- {m2} -")

    # Print the modified values if any
    print_values(modified, "Parámetros modificados", "No hay parámetros modificados")

    # Print the default values if any
    print_values(default, "Parámetros sin modificar", "No hay parámetros sin modificar")


# Main modify question function
def mod_question():
    print("\n\n\t\t-- MODIFICAR --\n¿Qué parámetro deseas modificar?")
    for a in parameters:
        print(f"\t- {a}")
    print(f"\n\t'{BACK[0].capitalize()}/{BACK[1].capitalize()}' para regresar.")
    mod_values()


# Function to filter the data entered by the user
def input_filter():
    input_user = input("\nRespuesta: ").lower()

    def ip_case():
        ip_input = input(f"\n¿Qué IP deseas modificar?\n\t- Server\n\t- Client\n\nRespuesta: ").lower()
        match ip_input:
            case "server":
                return "ip_server"
            case "s":
                return "ip_server"
            case "client":
                return "ip_client"
            case "c":
                return "ip_client"
            case "":
                print("\nNo has escrito nada. Intenta de nuevo.")
                return ip_case()
            case another:
                if another in [a.lower() for a in BACK]:
                    print("Regresando...")
                    mod_question()
                else:
                    print("\nLas opciones disponibles son Server/Client. Intenta de nuevo.")
                    return ip_case()

    match input_user:
        case "s":
            return "ssid"
        case "g":
            return "gate"
        case "m":
            return "mask"
        case other:
            if other in [a.lower() for a in PASS]:
                return "password"
            elif other in [a.lower() for a in SERVER]:
                return "ip_server"
            elif other in [a.lower() for a in CLIENT]:
                return "ip_client"
            elif other in [a.lower() for a in IP]:
                return ip_case()
            else:
                return input_user


# Modify values function
def mod_values():
    filtered_input = input_filter()
    if filtered_input in [a.lower() for a in BACK]:
        print("Regresando...")
        start()
    elif filtered_input == "":
        print("\nNo has escrito nada. Intenta de nuevo.")
        mod_values()
    elif filtered_input not in [a.lower() for a in parameters]:
        print(f"\n'{filtered_input}' no es un parámetro elegible. Intenta de nuevo.")
        mod_values()
    else:
        print(f"\n\t-- Modificando el parámetro '{filtered_input.upper()}' --\n"
              f"\n(Escribe '{BACK[0]}/{BACK[1]}' para regresar).")
        match filtered_input:
            case "ssid":
                change_ssid_pass("ssid")
            case "password":
                change_ssid_pass("password")
            case "ip_server":
                change_values("ip_server")
            case "gate":
                change_values("gate")
            case "mask":
                change_values("mask")
            case "ip_client":
                change_values("ip_client")


# Change IP, Gate & Mask values function
def change_values(name):
    print(f"\nValor actual: {parameters[name]}")
    input_user = input("Ingresa el nuevo valor: ")

    if input_user.lower() in [a.lower() for a in BACK]:
        print("Regresando...")
        mod_question()
    elif input_user == parameters[name]:
        print("Lo que has ingresado es igual al valor actual. Intenta de nuevo.")
        change_values(name)
    else:
        results = re.match(r"^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))).){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))$", input_user)
        if results:
            parameters[name] = results[0]
            print(f"\nFormato aceptado.\nNuevo valor: {parameters[name]}")
        else:
            print(f"\n'{input_user}' no cumple con el formato: '[0-254].[0-254].[0-254].[0-254]'. Intenta de nuevo.")
            change_values(name)


# Change SSID & Password values function
def change_ssid_pass(name):
    print(f"\nActual: {parameters[name]}")
    input_user = input("Nuevo: ")
    if input_user.lower() in [a.lower() for a in BACK]:
        print("Regresando...")
        mod_question()
    elif input_user == parameters[name]:
        print("Lo que has ingresado es igual al valor actual. Intenta de nuevo.")
        change_ssid_pass(name)
    else:
        if len(input_user) < 5:
            print(f"\nSe necesitan mínimo 5 caracteres, ingresaste {len(input_user)}. Intenta de nuevo.")
            change_ssid_pass(name)
        elif len(input_user) > 15:
            print(f"\nSe admite un máximo de 15 caracteres, ingresaste {len(input_user)}. Intenta de nuevo.")
            change_ssid_pass(name)
        else:
            parameters[name] = input_user
            if name == "ssid":
                print(f"\nEl nuevo SSID es: {parameters[name]}")
            else:
                print(f"\nLa nueva password es: {parameters[name]}")


# Function to save the file into the user path
def save_file():
    user_path = "C:\\Users\\Lasec\\PycharmProjects\\Lasec_Dev\\"
    file_name = "Smart_Lamp_Test.txt"
    file = open(user_path + file_name, "w")
    file.write("\t -- Smart Lamp 2v1 --\n\n")
    for x, y in parameters.items():
        file.write(f"\t- {x}: {y}")
    file.close()
    return file


# Function to get the user confirmation to entry into the tcp_server function
def tcp_server_confirm():
    print("\n\n\t\t-- SERVIDOR TCP --")
    # Check for any unmodified value and ask the user to continue
    if len(default) >= 1:
        print("\nAún quedan parámetros sin modificar:")
        # Print the default values if any
        list_dictionary(default)

        def question():
            input_user = input(f"\n¿Continuar aún así?\n"
                               f"Escribe:\n"
                               f"\t-'{YES[0]}/{YES[1]}' para confirmar.\n"
                               f"\t-'{NO[0]}/{NO[1]}' para regresar.\n"
                               f"\nRespuesta: ").lower()
            if input_user in [a.lower() for a in YES]:
                print("\n\t\t\t\t-- Iniciando servidor TCP/IP --")
                tcp_server()
            elif input_user in [b.lower() for b in NO]:
                start()
            else:
                print(f"\n'{input_user}' no es una respuesta válida. Intenta de nuevo.")
                question()

        question()
    else:
        print("\n\t\t\t\t-- Iniciando servidor TCP/IP --")
        tcp_server()


# Main function to create the TCP connection
def tcp_server():
    # Receive confirmation, send parameter function
    def recv_send(name, command, parameter):
        # Receive confirmation
        data_rs = conn.recv(1024).decode()
        print(f"\nRecibido: {data_rs}")
        print(f"Enviando {name}...")
        data_split_rs = data_rs.split("; ")
        message_rs = data_split_rs[1]
        time.sleep(1)

        # Send parameter
        if data_rs == ("MAC: " + mac + "; " + message_rs):
            conn.send((command + parameter).encode())

    # Connection values
    host_name = socket.gethostname()
    local_ip = socket.gethostbyname(host_name)  # IP address
    port = 8077  # Port to listen on
    socket_address = (local_ip, port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(30)
            # Bind and listen to the connection values
            s.bind(socket_address)
            s.listen(1)
            print(f"\nServidor con IP: {local_ip}\t\tPuerto: {port}")
            print("\nEsperando cliente...")

            # Client connection accept
            conn, addr = s.accept()
            with conn:

                # Print connected client values
                print(f"\nConectado con cliente:\nIP: {addr[0]}\t\tPuerto: {addr[1]}")
                time.sleep(1)

                # Receive and print MAC address
                data = conn.recv(1024).decode()
                mac = data
                print(f"\nMAC recibida: {mac}")

                def send_flash():
                    print(f"\nDato FLASH enviado...")
                    conn.send("FLASH".encode())

                def start_configuration():
                    print(f"\nEnviando mensaje {START_MESSAGE}...")
                    time.sleep(1)
                    # Send START_MESSAGE to the client
                    conn.send(START_MESSAGE.encode())

                    # Receive START_MESSAGE confirmation and send SSID
                    recv_send("SSID", commands["ssid_c"], parameters["ssid"])

                    # Receive SSID confirmation and send Password
                    recv_send("Password", commands["key_c"], parameters["password"])

                    # Receive Password confirmation and send IP server
                    recv_send("IP server", commands["ip_server_c"], parameters["ip_server"])

                    # Receive IP confirmation and send Gate
                    recv_send("Gate", commands["gate_c"], parameters["gate"])

                    # Receive Gate confirmation and send Mask
                    recv_send("Mask", commands["mask_c"], parameters["mask"])

                    # Receive Mask confirmation and send IP client
                    recv_send("IP client", commands["ip_client_c"], parameters["ip_client"])

                    # Receive IP confirmation
                    data_ip = conn.recv(1024).decode()
                    print(f"\nRecibido: {data_ip}")
                    print("\nEnviando comando 'Configuración completada'...")
                    data_split = data_ip.split("; ")
                    message = data_split[1]
                    time.sleep(1)

                    # Sending Reset command
                    if data_ip == ("MAC: " + mac + "; " + message):
                        conn.send(commands["succeed_c"].encode())
                        tcp_conf["Finished"] = True
                        print(f"\nConfiguración exitosa.")
                        s.close()
                    else:
                        tcp_conf["Finished"] = False
                    print("\nRegresando al inicio...")
                    start()

                def conn_init():
                    input_user = input(f"\n¿Qué deseas hacer?\n"
                                       f"\t- (1) Identificar.\n"
                                       f"\t- (2) Comenzar la configuración.\n"
                                       f"\nRespuesta: ")
                    if input_user == "1":
                        send_flash()
                        conn_init()
                    elif input_user == "2":
                        start_configuration()
                    else:
                        print(f"\n'{input_user}' no es una respuesta válida. Intenta de nuevo.")
                        conn_init()

                conn_init()

        except TimeoutError:
            s.close()
            print("\n\t\t\t\t-- Tiempo agotado. Reiniciando el servidor... --")
            tcp_server()
        except OSError as e:
            print(f"\nNo se pudo completar la configuración debido al siguiente error:\n\t- {e}\n"
                  "\nVolviendo al inicio...")
            s.close()
            start()


# Exit confirmation function
def exit_confirm():
    def exit_question():
        input_user = input(f"\n¿Deseas iniciar la conexión TCP con los valores actuales?\n"
                           f"Escribe:\n"
                           f"-\t'{SHOW[0]}/{SHOW[1]}' para mostrar los valores actuales.\n"
                           f"-\t'{YES[0]}/{YES[1]}' para confirmar.\n"
                           f"-\t'{NO[0]}/{NO[1]}' para regresar.\n"
                           f"\nRespuesta: ").lower()
        if input_user in [a.lower() for a in SHOW]:
            show_values()
            exit_question()
        elif input_user in [a.lower() for a in YES]:
            tcp_server_confirm()
        elif input_user in [a.lower() for a in NO]:
            start()
        else:
            print(f"\n'{input_user}' no es una respuesta válida. Intenta de nuevo.")
            exit_question()

    if tcp_conf["Finished"]:
        print("\nGuardando valores. Saliendo del programa...")
        save_file()
    else:
        print("\nAún no se ha completado la configuración.")
        exit_question()


# Main execution function
def start():
    input_user = ask_to_user().lower()
    if input_user in [a.lower() for a in MOD]:
        mod_question()
        start()
    elif input_user in [a.lower() for a in SHOW]:
        show_values()
        start()
    elif input_user in [a.lower() for a in TCP]:
        tcp_server_confirm()
    elif input_user in [a.lower() for a in EXIT]:
        exit_confirm()
    elif input_user == "":
        print("\nNo has escrito nada. Intenta de nuevo.")
        start()
    elif input_user in [a.lower() for a in BACK]:
        print("\nNo se puede retroceder más. Intenta de nuevo.")
        start()
    else:
        print(f"\n'{input_user}' no es una respuesta válida. Intenta de nuevo.")
        start()


# Main function
def main():
    try:
        welcome()
        start()
    except KeyboardInterrupt:
        print("\n\n\n\t\t>>>> Programa interrumpido por el usuario. Finalizando... <<<<")


# ----------------------------------------  Main block execution   ---------------------------------------- #
if __name__ == "__main__":
    main()
