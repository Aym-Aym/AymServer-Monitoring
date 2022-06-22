# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import QApplication

import socket
import sys
import errno
import threading
import time
import re
import ast
from psutil import boot_time, cpu_percent, disk_usage


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(os.fspath(Path(__file__).resolve().parent / "qml/main.qml"))

    """ Setup variables """

    HEADER = 10
    PORT = 5051
    FORMAT = 'utf-8'
    # SERVER = "192.168.1.60"
    SERVER = "127.0.0.1"
    ADDR = (SERVER, PORT)


    """ Connecting to socket server """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))
    # client_socket.setblocking(False)

    """ Authentication on the socket server """

    password = "password123"
    password_header = f"{len(password):<{HEADER}}{password}".encode(FORMAT)

    client_socket.send(password_header)

    message_size = client_socket.recv(HEADER)
    message_size = int(message_size)

    if not message_size:
        False

    message = client_socket.recv(message_size).decode(FORMAT)
    print(message)

    """ Creating receiving message thread function """

    def thread(client):
        try:
            while True:
                message_size = client.recv(HEADER)
                message_size = int(message_size)

                if not message_size:
                    False

                message = client.recv(message_size).decode(FORMAT)
                print(message)
                if re.match("(.+) ({.+})", message):
                    _, match = re.match("(.+) ({.+})", message).groups()
                    dictionary = ast.literal_eval(match)

                    engine.rootObjects()[0].setProperty("value_cpu", dictionary["cpu"])
                    engine.rootObjects()[0].setProperty("value_mem", dictionary["mem"])

                    #hdd = ast.literal_eval(dictionary["hdd"])
                    #print(hdd["percent"])

        except:
            print("connection closed...")

    """ Starting thread """

    thread = threading.Thread(target=thread, args=(client_socket,))
    thread.start()
    time.sleep(2)

    """ Requesting cpu and memory info from server """

    command_header = f"{len('!cpu'):<{HEADER}}!cpu".encode(FORMAT)
    client_socket.send(command_header)
    command_header = f"{len('!mem'):<{HEADER}}!mem".encode(FORMAT)
    client_socket.send(command_header)

    """ Disconnecting from socket when app is closed """

    def exit():
        command_header = f"{len('!disconnect'):<{HEADER}}!disconnect".encode(FORMAT)
        client_socket.send(command_header)
    app.aboutToQuit.connect(exit)

    sys.exit(app.exec_())
