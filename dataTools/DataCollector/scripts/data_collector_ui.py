import os
import re
import logging
import maya.cmds as cmd
from maya import OpenMayaUI

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
import shiboken2 as shiboken

import utils

main_window = None


def create():
    print 'Creating UI'
    global main_window
    if main_window is None:
        print 'Main Window is None'
        main_window = MainWindow()
        main_window.show()


def delete():
    print 'Deleting UI'
    global main_window
    if main_window is not None:
        print 'Main Window not None'
        main_window.close()
        main_window = None


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


# Main Window Class - Subclass of QtWidgets.QMainWindow
class MainWindow(QtWidgets.QMainWindow):
    # Output path to save the json data file
    working_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), u"out")
    # Loading path
    loading_path = ''
    # Controller Config Path
    ctrl_config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), u"ctrl_config.json")

    def __init__(self):

        super(MainWindow, self).__init__()

        if not os.path.exists(self.working_path):
            os.makedirs(self.working_path)

        # Load and config UI
        ui_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_collector.ui")
        self.ui = self.load_ui(ui_file_path)
        self.mayaWindow = self.get_maya_windows()
        self.ui.setParent(self.mayaWindow)
        self.ui.setWindowFlags(QtCore.Qt.Window)

        # Test Log Widget
        self.append_to_log_list(u'--- LOG WIDGET ---')

        # Add Output Path Modification Listeners
        self.ui.exportLocField.setText(self.working_path)
        self.ui.exportLocField.textChanged.connect(self.set_working_path)
        self.ui.exportLocField.returnPressed.connect(self.set_working_path)
        self.ui.exportLocField.cursorPositionChanged.connect(self.set_working_path)
        self.ui.exportLocField.selectionChanged.connect(self.set_working_path)

        # Add Loading Path Modification Listeners
        self.ui.dataLocField.setText(self.loading_path)
        self.ui.dataLocField.textChanged.connect(self.set_loading_path)
        self.ui.dataLocField.returnPressed.connect(self.set_loading_path)
        self.ui.dataLocField.cursorPositionChanged.connect(self.set_loading_path)
        self.ui.dataLocField.selectionChanged.connect(self.set_loading_path)

        # Add Browse Select Connection
        self.ui.browseExportLocationButton.clicked.connect(lambda: self.browse_callback(self.ui.exportLocField))
        self.ui.browseDataLocButton.clicked.connect(lambda: self.browse_callback(self.ui.dataLocField))

        # Add Debug List Clear Connection
        self.ui.clearLog.clicked.connect(self.clear_log_list)
        # Add Export Connection
        self.ui.exportButton.clicked.connect(self.export_callback)
        # Add Load Connection
        self.ui.loadButton.clicked.connect(self.load_callback)

        # Add EventFilter to Detect CloseEvent
        self.ui.installEventFilter(self)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance

    @staticmethod
    def load_ui(path):
        ui_file = QtCore.QFile(path)
        ui_file.open(QtCore.QFile.ReadOnly)
        ui_window = QtUiTools.QUiLoader().load(ui_file)
        ui_file.close()
        return ui_window

    @staticmethod
    def get_maya_windows():
        """
        Get Maya's main window.
        :rtype: QMainWindow
        """
        window = OpenMayaUI.MQtUtil.mainWindow()
        window = shiboken.wrapInstance(long(window), QtWidgets.QMainWindow)
        return window

    def set_working_path(self):
        self.working_path = self.ui.exportLocField.text()

    def set_loading_path(self):
        self.loading_path = self.ui.dataLocField.text()

    def show(self):
        self.ui.show()

    def eventFilter(self, ui, event):
        if ui is self.ui and event.type() == QtCore.QEvent.Close:
            self.append_to_log_list(u'--- Closing Main Window ---')
            self.ui.close()
            return True
        return False

    def show_predict_time(self, second):
        self.ui.label_3.setText(str(second) + "s")
        QtCore.QCoreApplication.processEvents()

    def append_to_log_list(self, log):
        self.ui.logWidget.addItem(log)
        self.ui.logWidget.scrollToBottom()
        QtCore.QCoreApplication.processEvents()

    def clear_log_list(self):
        self.ui.logWidget.clear()
        QtCore.QCoreApplication.processEvents()

    def export_callback(self):
        self.append_to_log_list('Exporting to ' + self.working_path)

    def browse_callback(self, text_field):
        self.append_to_log_list('Browsing path...')
        self.working_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        text_field.setText(self.working_path)
        self.append_to_log_list('Selected: ' + self.working_path)

    def load_callback(self):
        utils.json_load(str(self.ctrl_config_path))
        pass
