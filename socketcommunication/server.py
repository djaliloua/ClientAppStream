import socket
import struct


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




