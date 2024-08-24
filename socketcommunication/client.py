import socket
import struct


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
        try:
            self._sock.send(b"done")
        except:
            print("server not responding...")

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