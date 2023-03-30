import os
import re
import logging


from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
import shiboken2 as shiboken


main_window = None


def create():
    print ('Creating UI')
    global main_window
    if main_window is None:
        print ('Main Window is None')
        main_window = QtWidgets()
        main_window.show()


def delete():
    print ('Deleting UI')
    global main_window
    if main_window is not None:
        print ('Main Window not None')
        main_window.close()
        main_window = None


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton