import os.path
import socket
import struct
from dataclasses import dataclass
import cv2
import numpy as np
import flet as ft


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


LOCALHOST = get_ip()
# "192.168.1.212"
# print(ANDROID_IP)
LG_IP = "192.168.228.12"
PORT = 8888
RESOLUTION = (640, 480)
filename = "settings.json"


def save_json(page: ft.Page):
    import json

    with open(filename, 'w') as fp:
        json.dump({"ANDROID_IP":page.client_storage.get("ANDROID_IP")}, fp)
        # page.client_storage.set("ANDROID_IP", data["ANDROID_IP"])


def load_json_data(page: ft.Page):
    import json

    if not os.path.exists(filename):
        page.client_storage.set("ANDROID_IP", "")
        save_json(page)

    with open(filename, "r") as json_file:
        my_dict = json.load(json_file)
        page.client_storage.set("ANDROID_IP", my_dict["ANDROID_IP"])


def convert_to_frame(pixels, image_size):
    rgba = np.fromstring(pixels, np.uint8).reshape(image_size[1],
                                                   image_size[0], 4)
    frame = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
    ret, buffer = cv2.imencode('.jpg', rgba)
    frame = buffer.tobytes()

    return frame


class Server:

    def __init__(self, host, port, sock=None):
        self._host = host
        self._port = port
        self.is_error = False
        if sock is None:
            self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket_obj = sock
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # self._sock.setblocking(False)
        self._conn = None
        self._addr = None
        self.platform = None
        self.binding()
        self.accept()

    def binding(self):
        self.socket_obj.bind((self._host, self._port))
        self.socket_obj.listen()

    def accept(self):
        print("waiting for connection...")
        self._conn, self._addr = self.socket_obj.accept()
        print(f"{self._addr}")

    def send_bytes(self, pixels):
        if self._conn is not None:
            nbytes = len(pixels)
            # print(f'CLIENT: nBytes={nbytes}')
            # Send 4-byte network order frame size and image
            hdr = struct.pack('!i', nbytes)
            self._conn.sendall(hdr)
            self._conn.sendall(pixels)
            # Ack
            ack = self._conn.recv(1024).decode("utf-8")
            # print(ack)

    def receive_bytes(self):
        ack = self._conn.recv(1024).decode("utf-8")
        print(ack)
        if ack == "":
            print("hhh haha haha haha")
            self.is_error = True
        return ack

    def close_connection(self):
        self._conn.close()

    def close_socket(self):
        self.socket_obj.close()


@dataclass
class Data:
    data: bytes = None
    server: Server = None
    frame: bytes = None
    is_client_running: bool = True
    is_server_running: bool = True


class Client:
    def __init__(self, host, port, sock=None):
        self._host = host
        self._port = port
        self.is_connected = True
        self.is_error = False
        self._msg = ""
        if sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._sock = sock
        print(self._host)
        self._try_to_connect()

        # print(self._receive_bytes())

    def send_ack(self):
        self._sock.send(self._msg.encode("utf-8"))

    def send_done(self):
        self._sock.send(b"done")

    def _try_to_connect(self):
        while self.is_connected:
            try:
                print("Connecting to server.....")
                self._sock.connect((self._host, self._port))
                print("connected to the server.......")
                self.is_connected = not self.is_connected
            except Exception as ex:
                print(ex)

    def receive_bytes(self):
        try:
            # Get header with number of bytes
            header = self._sock.recv(4)
            nBytes = struct.unpack('!i', header)[0]
            # Receive actual image
            img = self._recvall(nBytes)
            self._msg = "ok"
            self._sock.send(self._msg.encode("utf-8"))
            return img
        except Exception as ex:
            self.is_error = True
            print(f"hello {ex}")
            # return

    def _recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = self._sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def close_socket(self):
        self._sock.close()
