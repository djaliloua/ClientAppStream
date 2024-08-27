import threading
from concurrent.futures import thread

import flet as ft
from UserControls.cameraControl import Camera
from UserControls.file import File
from utility.Utility import JsonHelper


class MainClass:
    def __init__(self):
        self.camera = None

    def main(self, page: ft.Page):
        page.title = "Video Stream Client"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.width = 700
        page.window.height = 750
        page.window.resizable = False
        page.window.maximizable = False
        page.window.frameless = False
        page.window.prevent_close = True
        page.window.center()
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.ALWAYS
        self.event = threading.Event()
        self.camera = Camera(self.event, page)
        self.jsonhelper = JsonHelper()

        def _on_window(e: ft.ControlEvent):
            if e.data == "close":
                self.event.set()
                self.camera.smart_close()
                page.window.destroy()



        page.window.on_event = _on_window
        self.jsonhelper.load_json_data(page)

        def get_row_control(ctrl, align):
            return ft.Container(
                content=ctrl,
            )

        def print_destination(e: ft.ControlEvent):

            if int(e.data) == 0:
                self.jsonhelper.load_json_data(page)
                page.controls[0] = get_row_control(self.camera, ft.MainAxisAlignment.CENTER)

            if int(e.data) == 1:
                page.controls[0] = get_row_control(File(page), ft.MainAxisAlignment.START)

            page.update()

        page.navigation_bar = ft.NavigationBar(
            on_change=print_destination,
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.CAMERA, label="Camera"),
                ft.NavigationBarDestination(icon=ft.icons.SAVE, label="Files"),
            ],

        )
        page.update()
        # file.visible = False
        page.add(get_row_control(self.camera, ft.MainAxisAlignment.CENTER))

    def run(self):
        ft.app(target=self.main)


if __name__ == "__main__":
    MainClass().run()
