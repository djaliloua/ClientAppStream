import os

import flet as ft
from UserControls.cameraControl import Camera, File
from utility.Utility import load_json_data


class MainClass:
    def __init__(self):
        self.camera = None

    def main(self, page: ft.Page):
        page.title = "Video Stream Client"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window_width = 700
        page.window_height = 750
        page.window_resizable = False
        page.window_maximizable = False
        page.window_frameless = True
        page.window_prevent_close = True
        page.window_center()
        page.theme_mode = ft.ThemeMode.DARK
        page.scroll = ft.ScrollMode.ALWAYS
        self.camera = Camera(page)

        def _on_window(e: ft.ControlEvent):
            if e.data == "close":
                self.camera.smart_close()
                page.window_destroy()

        page.on_window_event = _on_window
        load_json_data(page)

        def get_row_control(ctrl, align):
            return ft.Container(
                content=ctrl,
            )

        def print_destination(e: ft.ControlEvent):

            if int(e.data) == 0:
                load_json_data(page)
                # page.controls.pop(0)
                # page.controls.append(get_row_control(self.camera, ft.MainAxisAlignment.CENTER))
                page.controls[0] = get_row_control(self.camera, ft.MainAxisAlignment.CENTER)

            if int(e.data) == 1:
                page.controls[0] = get_row_control(File(page), ft.MainAxisAlignment.START)

            page.update()

        page.navigation_bar = ft.NavigationBar(
            on_change=print_destination,
            destinations=[
                ft.NavigationDestination(icon=ft.icons.CAMERA, label="Camera"),
                ft.NavigationDestination(icon=ft.icons.SAVE, label="Files"),
            ],

        )

        page.update()
        print(page.navigation_bar.data)

        # file.visible = False
        page.add(get_row_control(self.camera, ft.MainAxisAlignment.CENTER))

    def run(self):
        ft.app(target=self.main)


if __name__ == "__main__":
    MainClass().run()
