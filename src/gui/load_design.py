import sys

from os import path

from PyQt5 import QtWidgets, uic


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, file_path: str):
        super().__init__()
        if not path.isfile(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        uic.loadUi(file_path, self)
        self.show()


def window(file_path: str) -> None:
    app = QtWidgets.QApplication([])
    win = MyWindow(file_path)
    win.show()
    sys.exit(app.exec_())
