import os
import re
import logging
import sys

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
import shiboken2 as shiboken

import data_process_utils

main_window = None


def create():
    print('Creating UI')
    global main_window
    if main_window is None:
        print('Main Window is None')
        main_window = QtWidgets()
        main_window.show()


def delete():
    print('Deleting UI')
    global main_window
    if main_window is not None:
        print('Main Window not None')
        main_window.close()
        main_window = None


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


class MainWindow(QtWidgets.QMainWindow):
    # Ctrl Config path
    ctrl_config_path = ''
    # Data Loading path
    data_loading_path = ''
    # Img Loading path
    img_loading_path = ''
    # Output path
    export_path = ''

    def __init__(self):

        super(MainWindow, self).__init__()

        '''
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
        '''

        # Load and config UI
        ui_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_process.ui")
        self.ui = self.load_ui(ui_file_path)
        self.ui.setWindowFlags(QtCore.Qt.Window)

        # Test Log Widget
        self.append_to_log_list(u'--- LOG WIDGET ---')

        # Add Output Path Modification Listeners
        self.ui.exportLocField.setText(self.export_path)
        self.ui.exportLocField.textChanged.connect(self.set_export_path)
        self.ui.exportLocField.returnPressed.connect(self.set_export_path)
        self.ui.exportLocField.cursorPositionChanged.connect(self.set_export_path)
        self.ui.exportLocField.selectionChanged.connect(self.set_export_path)

        # Add Controllers Config Loading Path Modification Listeners
        self.ui.ctrlConfigLocField.setText(self.ctrl_config_path)
        self.ui.ctrlConfigLocField.textChanged.connect(self.set_ctrl_config_path())
        self.ui.ctrlConfigLocField.returnPressed.connect(self.set_ctrl_config_path)
        self.ui.ctrlConfigLocField.cursorPositionChanged.connect(self.set_ctrl_config_path)
        self.ui.ctrlConfigLocField.selectionChanged.connect(self.set_ctrl_config_path)

        # Add Controllers Data Loading Path Modification Listeners
        self.ui.dataLocField.setText(self.data_loading_path)
        self.ui.dataLocField.textChanged.connect(self.set_data_loading_path)
        self.ui.dataLocField.returnPressed.connect(self.set_data_loading_path)
        self.ui.dataLocField.cursorPositionChanged.connect(self.set_data_loading_path)
        self.ui.dataLocField.selectionChanged.connect(self.set_data_loading_path)

        # Add Img Data Loading Path Modification Listeners
        self.ui.imgLocField.setText(self.img_loading_path)
        self.ui.imgLocField.textChanged.connect(self.set_img_loading_path)
        self.ui.imgLocField.returnPressed.connect(self.set_img_loading_path)
        self.ui.imgLocField.cursorPositionChanged.connect(self.set_img_loading_path)
        self.ui.imgLocField.selectionChanged.connect(self.set_img_loading_path)

        # Add Browse Select Connection
        self.ui.browseCtrlConfigLocButton.clicked.connect(self.browse_ctrl_config_load_callback)
        self.ui.browseDataLocButton.clicked.connect(self.browse_data_load_callback)
        self.ui.browseImgLocButton.clicked.connect(self.browse_img_load_callback)
        self.ui.browseExportLocButton.clicked.connect(lambda: self.browse_callback(self.ui.exportLocField))

        # Add Load Connection
        self.ui.loadButton.clicked.connect(self.load_callback)

        # Add Generate Connection
        self.ui.generateButton.clicked.connect(self.generate_callback)

        # Add Debug List Clear Connection
        self.ui.clearLog.clicked.connect(self.clear_log_list)

        # Add EventFilter to Detect CloseEvent
        self.ui.installEventFilter(self)

    def load_ui(self, file_path):
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(file_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        ui = loader.load(ui_file)
        ui_file.close()
        return ui

    def instance(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance

    def set_export_path(self):
        self.export_path = self.ui.exportLocField.text()

    def set_ctrl_config_path(self):
        self.ctrl_config_path = self.ui.ctrlConfigLocField.text()

    def set_img_loading_path(self):
        self.img_loading_path = self.ui.imgLocField.text()

    def set_data_loading_path(self):
        self.data_loading_path = self.ui.dataLocField.text()

    def show(self):
        self.ui.show()

    def eventFilter(self, ui, event):
        if ui is self.ui and event.type() == QtCore.QEvent.Close:
            self.append_to_log_list(u'--- Closing Main Window ---')
            # event.ignore()
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

    def generate_callback(self):
        data_process_utils.data_process(self.export_path)
        self.append_to_log_list('Plz Wait! Processing...')
        self.append_to_log_list('Generate to ' + self.export_path)

    def browse_callback(self, text_field):
        self.append_to_log_list('Browsing path...')
        self.export_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        text_field.setText(self.export_path)
        self.append_to_log_list('Selected: ' + self.export_path)

    def browse_ctrl_config_load_callback(self):
        self.append_to_log_list('Browsing controller config loading path...')
        self.ctrl_config_path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        self.ui.ctrlConfigLocField.setText(self.ctrl_config_path)
        self.append_to_log_list('Selected: ' + self.ctrl_config_path)

    def browse_data_load_callback(self):
        self.append_to_log_list('Browsing data loading path...')
        self.data_loading_path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        self.ui.dataLocField.setText(self.data_loading_path)
        self.append_to_log_list('Selected: ' + self.data_loading_path)

    def browse_img_load_callback(self):
        self.append_to_log_list('Browsing img loading path...')
        self.img_loading_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.ui.imgLocField.setText(self.img_loading_path)
        self.append_to_log_list('Selected: ' + self.img_loading_path)

    def load_callback(self):
        self.append_to_log_list('Loading controller config data...')
        data_process_utils.load_ctrl_config_file(self.ctrl_config_path)
        data_process_utils.load_ctrl_data(self.data_loading_path)


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
