from MainWin import MainWin
from Ui_main import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from math import *
import sys

if __name__ == "__main__":
    app=QApplication(sys.argv)
    win = MainWin()
    win.show()
    app.exec_()