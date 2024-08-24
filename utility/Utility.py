import os.path
import socket

import cv2
import flet as ft
import numpy as np


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



class JsonHelper:

    def load_json_data(self, page: ft.Page):
        import json

        if not os.path.exists(filename):
            page.client_storage.set("ANDROID_IP", "")
            self.save_json(page)

        with open(filename, "r") as json_file:
            my_dict = json.load(json_file)
            page.client_storage.set("ANDROID_IP", my_dict["ANDROID_IP"])


    def save_json(self, page: ft.Page):
        import json
        with open(filename, 'w') as fp:
            json.dump({"ANDROID_IP": page.client_storage.get("ANDROID_IP")}, fp)
            # page.client_storage.set("ANDROID_IP", data["ANDROID_IP"])


# def save_json(page: ft.Page):
#     import json
#
#     with open(filename, 'w') as fp:
#         json.dump({"ANDROID_IP":page.client_storage.get("ANDROID_IP")}, fp)
#         # page.client_storage.set("ANDROID_IP", data["ANDROID_IP"])
#
#
# def load_json_data(page: ft.Page):
#     import json
#     if not os.path.exists(filename):
#         page.client_storage.set("ANDROID_IP", "")
#         save_json(page)
#
#     with open(filename, "r") as json_file:
#         my_dict = json.load(json_file)
#         page.client_storage.set("ANDROID_IP", my_dict["ANDROID_IP"])


def convert_to_frame(pixels, image_size):
    rgba = np.fromstring(pixels, np.uint8).reshape(image_size[1],
                                                   image_size[0], 4)
    frame = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
    ret, buffer = cv2.imencode('.jpg', rgba)
    frame = buffer.tobytes()

    return frame


