import socket
from threading import Thread
from datetime import datetime
from monitor import Monitor
from exceptions import ReadClientException, SendClientException
from typing import Union


class Server:
    """ Create a socket server to send monitoring data to a client.

    Commands are !cpu, !mem, !hdd, !disconnect.

    More to come...
    """

    def __init__(self) -> None:
        super(Server, self).__init__()

        # Initialize default vars.

        self.HEADER = 10
        self.SERVER_IP = "127.0.0.1"
        self.PORT = 5051
        self.address = (self.SERVER_IP, self.PORT)
        self.FORMAT = "utf-8"
        self.client_disconnect = "!disconnect"
        self.server_password = "password123"
        self.SERVER_STARTED = False

        # Create socket server.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.address)

        self.clients_dict = dict()

        # Start server.
        self.start()

    def start(self) -> None:
        """Starts the server."""
        self.SERVER_STARTED = True

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[srv]  "\
                  f"[{date}]  "\
                  f"[starting]  "\
                  f"server {self.SERVER_IP} is starting..."
        print(message)
        self.logs(message)

        self.server.listen(5)
        message = f"[srv]  "\
                  f"[{date}]  "\
                  f"[listening]  "\
                  f"server {self.SERVER_IP} is now listening..."
        print(message)
        self.logs(message)

        # Waiting for client to connect and send commands.
        while self.SERVER_STARTED:
            # Get the client socket object and client address (ip, port).
            client_socket, client_address = self.server.accept()

            self.clients_dict[client_socket] = list()

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"[srv]  "\
                      f"[{date}]  "\
                      f"[client {client_address[0]}:{client_address[1]}]  "\
                      f"new client is trying to connect..."
            print(message)
            self.logs(message)

            message = f"connected to server {self.SERVER_IP}...\n" \
                      "waiting for authentication..."

            self.send(client_socket, message)

            # Authenticating client.
            auth = self.authentication(client_socket=client_socket)
            # If auth failed, disconnect client.
            if not auth:
                reason = "failed to authenticate"
                self.disconnect(
                    client_socket=False,
                    client_address=client_address,
                    message=reason
                )
                self.stats()
                client_socket.close()
                continue
            else:
                message = "[srv]  " \
                          f"[{date}]  " \
                          f"[client {client_address[0]}:{client_address[1]}]  " \
                          "authentication succeed..."
                print(message)
                self.logs(message)
                self.stats()

            self.client(client_socket, client_address)

    def client(self, client_socket: socket.socket, client_address: tuple) -> None:
        """Deals with sending clients requested datas.

        Args:
            client_socket (socket.socket): Client socket object.
            client_address (tuple): Client address in format (IP, PORT).
        """
        connected = True

        message = "you are now connected..."
        self.send(client_socket, message)

        thread_read = Thread(
            target=self.thread,
            args=(client_socket, client_address)
        )
        thread_read.start()

        monitor = Monitor(1)

        # While the client stays connected.
        while connected:
            connected = thread_read.is_alive()
            if client_socket in self.clients_dict.keys():
                if self.clients_dict[client_socket]:
                    to_send = {}
                    for command in self.clients_dict[client_socket]:
                        if command == "cpu":
                            to_send["cpu"] = f"{str(monitor.get_cpu())}"
                        elif command == "hdd":
                            to_send["hdd"] = monitor.get_hdd()
                        elif command == "sys":
                            to_send["sys"] = monitor.get_system()
                        elif command == "mem":
                            to_send["mem"] = monitor.get_mem()

                    self.send(client_socket, message=to_send, log=False)

    def thread(self, client_socket: socket.socket, client_address: tuple) -> None:
        """Create a thread to receive client requests.

        Args:
            client_socket (socket.socket): Client socket object.
            client_address (tuple): Client address in format (IP, PORT).
        """
        while True:
            command = self.read(client_socket)

            if not command:
                message = "not responding"
                self.disconnect(client_socket, client_address, message)
                self.clients_dict.pop(client_socket)
                client_socket.close()
                self.stats()
                break

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = "[rcv]  "\
                      f"[{date}]  "\
                      f"[client {client_address[0]}:{client_address[1]}]  "\
                      f"command: {command}"
            print(message)
            self.logs(message)

            # Check commands received from the client.
            # And update the clients dict that contains the list of data to send.
            if command == "!disconnect":
                message = "client request"
                self.disconnect(client_socket, client_address, message)
                self.clients_dict.pop(client_socket)
                client_socket.close()
                self.stats()
                break
            elif command == "!cpu":
                self.clients_dict[client_socket].append("cpu")
                message = f"[srv]  "\
                          f"[{date}]  "\
                          f"[send request]  "\
                          f"sending cpu monitoring stats to client {client_address[0]}:{client_address[1]}..."
                print(message)
                self.logs(message)
            elif command == "!hdd":
                self.clients_dict[client_socket].append("hdd")
                message = f"[srv]  "\
                          f"[{date}]  "\
                          f"[send request]  "\
                          f"sending hdd monitoring stats to client {client_address[0]}:{client_address[1]}..."
                print(message)
                self.logs(message)
            elif command == "!sys":
                self.clients_dict[client_socket].append("sys")
                message = f"[srv]  "\
                          f"[{date}]  "\
                          f"[send request]  "\
                          f"sending system info to client {client_address[0]}:{client_address[1]}..."
                print(message)
                self.logs(message)
            elif command == "!mem":
                self.clients_dict[client_socket].append("mem")
                message = f"[srv]  "\
                          f"[{date}]  "\
                          f"[send request]  "\
                          f"sending memory info to client {client_address[0]}:{client_address[1]}..."
                print(message)
                self.logs(message)
            elif command == "!stop":
                self.clients_dict[client_socket] = list()
                message = f"[srv]  "\
                          f"[{date}]  "\
                          f"[stop request]  "\
                          f"stopping all send to client {client_address[0]}:{client_address[1]}..."
                print(message)
                self.logs(message)

                message = "stopping all send..."
                self.send(client_socket, message)
            else:
                self.send(client_socket, "unknown command...")

    def read(self, client_socket: socket.socket) -> Union[str, bool]:
        """Reads requests from client.

        Args:
            client_socket (socket.socket): Client socket object.
        """
        try:
            message_size = client_socket.recv(self.HEADER)
            message_size = int(message_size)

            if not message_size:
                return "none"

            message = client_socket.recv(message_size).decode(self.FORMAT)

            return str(message)

        except ReadClientException:
            return False

    def send(
        self,
        client_socket: socket.socket,
        message: str,
        who: str = "server response",
        log: bool = True
    ) -> bool:
        """Sending data to client.

        Args:
            client_socket (socket.socket): Client socket object.
            message (str): Message to send to the client.
            who (str): Who is sending the message.
            log (bool): Are we loggin the message.

        Returns:
            bool: True if message was sent else False.
        """
        try:
            if who == "server response":
                who = f"server {self.SERVER_IP}:{self.PORT}"

            message = str(message)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message_lines = message.split("\n")

            new_message_lines = [
                f"[{date}]  [{who}]  {message}"
                for message in message_lines
            ]
            join_with = "\n"
            new_message = join_with.join(new_message_lines)

            if log:
                self.logs(f"[snd]  {new_message}")

            # Encoding the message then send it.
            message = new_message.encode("utf-8")
            message_header = f"{len(message):<{self.HEADER}}".encode("utf-8")
            client_socket.send(message_header + message)

            return True

        except SendClientException:
            return False

    def authentication(self, client_socket: socket.socket) -> bool:
        """Authenticate the client.

        Args:
            client_socket (socket.socket): Client socket object.

        Returns:
            bool: True if the client is authenticated else False.
        """
        password = self.read(client_socket)  # Read password sent by the client.

        if password == self.server_password:
            message = "authentication succeeded..."
            self.send(client_socket, message)
            return True
        else:
            message = "authentication failed...\n" \
                      f"disconnected from server {self.SERVER_IP}..."
            self.send(client_socket, message)

            if client_socket in self.clients_dict.keys():
                self.clients_dict.pop(client_socket)

            return False

    def disconnect(
        self,
        client_socket: socket.socket,
        client_address: tuple,
        message: str
    ) -> None:
        """Disconnecting the client.

        Args:
            client_socket (socket.socket): Client socket object.
            client_address (tuple): Client address in format (IP, PORT).
            message (str): Tell client that he has been disconnected.
        """
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if client_socket:
            message_send = f"disconnected from server {self.SERVER_IP}..."
            self.send(client_socket, message_send)

        message = f"[srv]  "\
                  f"[{date}]  "\
                  f"[client "\
                  f"{client_address[0]}:{client_address[1]}]  "\
                  f"disconnected: {message}..."
        print(message)
        self.logs(message)

    def stats(self) -> None:
        """Print server stats."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[srv]  "\
                  f"[{date}]  "\
                  f"[server stats]  "\
                  f"number of connected clients: {len(self.clients_dict)}"
        print(message)
        self.logs(message)

    def logs(self, log):
        log
        # print(f"logged: {log}")
