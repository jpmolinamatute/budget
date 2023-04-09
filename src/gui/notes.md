# GUI

1. QVBoxLayout: create horizonal or vertical layouts, this can be useful to create sections and subsections.
2. "Line Edit" is the input field equivalent.
3. "Text Edt" is the text area equivalent.
4. We can import and "load" *.ui files in our code/class  by doing:

    ```py
    from PyQt5 import QtWidgets, uic


    class MyWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super(MyWindow, self).__init__()
            uic.loadUi("./window.ui", self)
            self.show()
    ```

5. ui.* files are just XML file used as recipe
