#!/usr/bin/env python

import logging
import random
import sys

from os import path
from typing import Optional

from PySide6 import QtCore, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)
        self.setWindowTitle("MyWidget")
        self.resize(640, 480)
        self.show()

    @QtCore.Slot()
    def magic(self) -> None:
        self.text.setText(random.choice(self.hello))


def run() -> None:
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    sys.exit(app.exec())


def main() -> None:
    exit_status = 0
    logging.basicConfig(level=logging.DEBUG)
    try:
        logging.info("Script %s has started", path.basename(__file__))
        run()
        logging.info("Bye!")
    except Exception as err:
        logging.exception(err)
        exit_status = 1
    finally:
        sys.exit(exit_status)


if __name__ == "__main__":
    main()
