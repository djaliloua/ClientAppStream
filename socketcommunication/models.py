from dataclasses import dataclass



@dataclass
class Data:
    data: bytes = None
    server = None
    frame: bytes = None
    is_client_running: bool = True
    is_server_running: bool = True

@dataclass
class ClientPayLoad:
    payload: bytes = None
    is_client_running: bool = True
    is_server_running: bool = True
