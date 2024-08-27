import os
import subprocess
import flet
from UserControls.model import FileData


class File(flet.UserControl):
    def __init__(self, page: flet.Page):
        super().__init__()
        self.page = page

        self.list_items = flet.Column(scroll=flet.ScrollMode.ALWAYS,
                                      expand=False,
                                      )
        self.init()

    def build(self):
        return self.list_items

    def init(self):

        if not os.path.exists(r"VideoDesktopClient.exe"):
            folder = r"assets"
        else:
            folder = os.path.join(os.getcwd(), "assets")
        if not os.path.exists(folder):
            os.mkdir(folder)
        files = [FileData(name) for name in os.listdir(folder)]
        if os.path.exists(folder):
            for name in files:
                self.list_items.controls.append(flet.Row(
                    [flet.Icon(name.Icon_Name, tooltip=name.Extension), flet.Text(name.Name, tooltip=name.File_Name),
                     flet.Text(name.Extension),
                     flet.IconButton(flet.icons.OPEN_WITH, data=name,
                                     tooltip="Open",
                                     on_click=self._on_open),
                     flet.IconButton(flet.icons.DELETE,
                                     tooltip="Delete",
                                     data=name, on_click=self.on_delete)],
                    data=name, alignment=flet.MainAxisAlignment.SPACE_EVENLY))
        self.list_items.controls.reverse()

    def _on_open(self, e: flet.ControlEvent):
        filename = os.path.join(os.getcwd(), "assets", e.control.data.File_Name)
        # os.system(filename)
        subprocess.run([filename], shell=True)

    def on_delete(self, e):
        self.delete(e.control.data)

    def delete(self, name: FileData):
        folder = os.path.join(os.getcwd(), "assets")
        for ctrl in self.list_items.controls:
            if ctrl.data == name:
                os.remove(os.path.join(folder, name.File_Name))
                self.list_items.controls.remove(ctrl)
                self.update()