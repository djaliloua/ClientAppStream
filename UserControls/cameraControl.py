import base64
import os
import subprocess
import threading
from datetime import datetime as d
import cv2
import flet as ft
import moviepy.video.io.ImageSequenceClip
import numpy as np
from socketcommunication.client import Client
from socketcommunication.models import ClientPayLoad
from utility.Utility import PORT, JsonHelper
from logginghelper.logginghelper import Logging


def restart():
    if os.path.exists("VideoDesktopClient.exe"):
        subprocess.run(["VideoDesktopClient.exe"])
    else:
        os.system("py main.py")


class Camera(ft.Column):
    def __init__(self,event: threading.Event, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.logging = Logging()
        self._event = event
        self.running = True
        self.client_payload = ClientPayLoad()
        self._properties_initialization()
        self._control_initialization()
        self.update()

    def build(self):
        return ft.Column([
            ft.Row([self.ip_btn_label_edit, self.state, self.saving_text]),
            ft.Row([self.img]),
            ft.Row(
                [
                    ft.IconButton(icon=ft.icons.PHOTO_CAMERA, on_click=self._on_take_picture),
                    # ft.ElevatedButton("Take picture", on_click=self._on_take_picture),
                    ft.IconButton(icon=ft.icons.VIDEO_CAMERA_FRONT, on_click=self._on_take_video),
                    # ft.ElevatedButton("close", on_click=self.on_close)
                ]
            )

            # ft.ElevatedButton("Take picture", on_click=self._on_take_picture)
        ])

    def _properties_initialization(self):
        self.is_video = False
        self.fps = 20
        self.list_images = []
        self.RESOLUTION = [640, 480]
        self.size = None
        self.frame = None
        self.is_saving_video = False
        self.picture_count = 0
        self.state_message = ""
        self.text = 'Click to set ip address'
        self.jsonhelper = JsonHelper()

    def _control_initialization(self):
        self.img = ft.Image()
        self.pr = ft.ProgressRing(stroke_width=10)
        self.txt = ft.Text("Camera")
        self.page.on_close = self.on_close
        self.ip_textfield_value = ft.TextField()
        self.ip_label = ft.Text(f"{self.page.client_storage.get('ANDROID_IP')}", size=10)
        self.ip = self.page.client_storage.get('ANDROID_IP')
        self.ip_btn_label_edit = ft.TextButton(f"{self.ip if self.ip else self.text}",
                                               on_click=self.open_dlg_modal,
                                               tooltip="Edit IP address")
        self.save_btn = ft.TextButton("Save", on_click=self.on_save, autofocus=True)
        # self.ip_textfield_value.on_blur = self.on_blur_text_field
        # self.ip_textfield_value.on_focus = self.on_focus_text_field
        # self.page.on_keyboard_event = self.on_keyboard
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Set Values"),
            content=self.ip_textfield_value,
            actions=[
                ft.TextButton("Cancel", on_click=self.on_cancel),
                self.save_btn,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.saving_text = ft.Text(color=ft.colors.GREEN)
        self.page.dialog = self.dlg_modal
        self.state = ft.Text()

    def on_keyboard(self, e: ft.KeyboardEvent):
        pass
        # data = json.loads(e.data)
        # if self.ip_textfield_value.autofocus:
        #     if data["key"] == "Enter":
        #         self.ip_btn_label_edit.text = self.ip_textfield_value.value
        #         self.page.client_storage.set("ANDROID_IP", self.ip_textfield_value.value)
        #         save_json(self.page)
        #         self.close_dlg()
        #         self.page.window_destroy()
        #         self.update()
        #         restart()

    def on_focus_text_field(self, e):
        self.save_btn.autofocus = False
        self.ip_textfield_value.autofocus = True
        self.update()

    def on_blur_text_field(self, e):
        self.save_btn.autofocus = True
        self.save_btn.focus()
        self.ip_textfield_value.autofocus = False
        self.update()

    def state_color(self, message: str) -> None:
        self.state.value = message
        if self.state.value == "connected":
            self.state.color = ft.colors.GREEN
        else:
            self.state.color = ft.colors.RED

        self.update()

    def _save_video_status(self, message: str) -> None:
        self.saving_text.value = message
        self.update()

    def on_save(self, e: ft.ControlEvent):
        self.ip_btn_label_edit.text = self.ip_textfield_value.value
        self.page.client_storage.set("ANDROID_IP", self.ip_textfield_value.value)
        self.jsonhelper.save_json(self.page)
        self.close_dlg()
        self.page.window_destroy()
        self.update()
        restart()

    def on_cancel(self, e: ft.ControlEvent):
        self.close_dlg()

    def open_dlg_modal(self, e):
        if self.ip:
            self.ip_textfield_value.value = self.ip_btn_label_edit.text
        else:
            self.ip_textfield_value.hint_text = "Insert IP Address"
        self.dlg_modal.open = True
        self.page.update()

    def close_dlg(self):
        self.dlg_modal.open = False
        self.page.update()

    def on_close(self, e):
        self.close()
        self.client.close_socket()
        self.page.window_close()
        print("closing......")

    def smart_close(self):
        self.close()
        try:
            if self.client is not None:
                self.client.close_socket()
            print("closing......")
        except:
           if self.page is not None:
               self.page.window_destroy()

    def close(self):
        try:
            if self.client is not None:
                self.client.send_done()
                self.client.is_error = True
                self.client_payload.is_client_running = False

        except AttributeError as ex:
            pass

    def _on_take_picture(self, e):
        if not os.path.exists("assets"):
            os.mkdir("assets")

        if self.frame is not None:
            date = d.now()
            filename = date.strftime("%Y_%m_%d_%H_%M_%S")
            cv2.imwrite(os.path.join("assets", f"{filename}.png"), self.frame)
            self.page.snack_bar = ft.SnackBar(ft.Text("Captured"))
            self.page.snack_bar.open = True
            self.update()
        self.picture_count += 1
        self._save_video_status(f"captured({self.picture_count})...")

    def set_event(self):
        self.client_payload.is_client_running = False
        self._event.set()

    def _on_take_video(self, e):
        if not os.path.exists("assets"):
            os.mkdir("assets")
        self.is_video = not self.is_video

        if self.is_video:
            print("start recording")
            self._save_video_status("start recording...")
            self.logging.info("start recording...")
            self.list_images.clear()
        else:
            print("stop recording")
            self.logging.info("stop recording")
            if self.list_images:
                save_thread = threading.Thread(target=self._save_video, args=[])
                save_thread.start()

    def _save_video(self):
        date = d.now()
        filename = date.strftime("%Y_%m_%d_%H_%M_%S")
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(self.list_images, fps=self.fps)
        self.is_saving_video = True
        self._save_video_status("saving....")
        self.logging.info("saving....")
        clip.write_videofile(os.path.join("assets", f'{filename}.mp4'))
        self._save_video_status("saved")
        self.logging.info("saved")
        self.is_saving_video = False

    def _run_client(self):
        while self.client_payload.is_client_running and not self._event.is_set():

            if self.page:
                self.client = Client(self.page.client_storage.get("ANDROID_IP"), PORT)
                while not self.client.is_error and not self._event.is_set():
                    self.client_payload.payload = self.client.receive_bytes()

    def did_mount(self) -> None:
        self.running = True
        t = threading.Thread(target=self._update)
        t1 = threading.Thread(target=self._run_client)
        t1.start()
        t.start()

    def will_unmount(self) -> None:
        self.running = False
        self.close()

    def _update(self):
        while not self._event.is_set():
            try:
                if self.client_payload.payload is not None:
                    self.client_payload.is_client_running = True
                    self.state_color("connected")
                    self.logging.info("connected")
                    jpg_as_np = np.frombuffer(self.client_payload.payload, dtype=np.uint8).reshape(self.RESOLUTION[1],
                                                                                                   self.RESOLUTION[0],
                                                                                                   -1)
                    image = cv2.cvtColor(jpg_as_np, cv2.COLOR_BGRA2RGBA)
                    image = cv2.flip(image, 1)
                    self.frame = cv2.rotate(image, cv2.ROTATE_180)
                    # self.frame = jpg_as_np
                    self.frame = cv2.putText(self.frame, "Recording", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                             1,
                                             (0, 0, 255),
                                             1, cv2.LINE_AA) if self.is_video else self.frame
                    # cv2.imshow("title", self.frame)
                    retval, buffer = cv2.imencode('.jpg', self.frame)
                    buffer1 = base64.b64encode(buffer.tobytes()).decode()
                    self.img.src_base64 = buffer1
                    self.ip_btn_label_edit.disabled = self.client_payload.is_client_running
                    self.update()
                else:
                    self.client_payload.is_client_running = False
                    self.ip_btn_label_edit.disabled = self.client_payload.is_client_running
                    self.state_color("disconnected")
                    self.logging.info("disconnected")
                    self.update()
            except Exception as ex:
                try:
                    self.client_payload.is_client_running = False
                    self.ip_btn_label_edit.disabled = self.client_payload.is_client_running
                    self.state_color("disconnected")
                    self.logging.info("disconnected")
                    self.update()
                    print(ex)
                except:
                    pass
            if self.is_video:
                if self.frame is not None:
                    self.list_images.append(self.frame)
            # time.sleep(1 / 33.0)




# flet pack main.py --icon icon.ico --name VideoDesktopClient --product-name StreamingVideo --product-version 4.0.0.0
# --company-name Personal
