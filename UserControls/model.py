import os.path


class FileData:
    def __init__(self, filename: str):
        self.File_Name = filename
        self.Extension = "Picture" if self.File_Name.endswith(".png") else "Video"
        self.Name = os.path.splitext(self.File_Name)[0]
        self.Icon_Name = "image" if self.File_Name.endswith(".png") else "camera"