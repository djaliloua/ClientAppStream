import os

import flet as ft
from UserControls.cameraControl import Camera, File
from utility.Utility import load_json_data


class Nav(ft.NavigationDestination):
    def _build(self):
        st = ft.Stack([
            ft.Container(
                content=ft.CircleAvatar(bgcolor=ft.colors.RED, radius=5),
                alignment=ft.alignment.top_right,
            ),
            ft.Container(
                content=ft.NavigationDestination(icon=ft.icons.SAVE, label="Files"),
                bgcolor=ft.colors.BLUE
            )
        ])
        return st


def main(page: ft.Page):
    page.title = "Video Stream Client"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 700
    page.window_height = 750
    page.window_resizable = False
    page.window_maximizable = False
    page.window_frameless = True
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS
    load_json_data(page)
    camera = Camera(page)

    def get_row_control(ctrl, align):
        return ft.Container(
            content=ctrl,

        )

    def print_destination(e: ft.ControlEvent):

        if int(e.data) == 0:
            load_json_data(page)
            page.controls[0] = get_row_control(camera, ft.MainAxisAlignment.CENTER)

        if int(e.data) == 1:
            page.controls[0] = get_row_control(File(), ft.MainAxisAlignment.START)

        page.update()
    st = ft.Stack(
        [
            ft.NavigationDestination(icon=ft.icons.SAVE, label="Files")
        ],
        width=20,
        height=20

    )
    page.navigation_bar = ft.NavigationBar(
        on_change=print_destination,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.CAMERA, label="Camera"),
            ft.NavigationDestination(icon=ft.icons.SAVE, label="Files"),
        ],

    )

    page.update()

    # file.visible = False
    page.add(get_row_control(camera, ft.MainAxisAlignment.CENTER))


if __name__ == "__main__":
    ft.app(target=main)
