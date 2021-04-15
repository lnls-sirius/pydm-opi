from qtpy import QtWidgets, QtCore, uic
from pydm import Display

from qtpy.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication

import paramiko
import pandas
import requests
import sys
import logging
import urllib3

from models import TableModel, PvTableModel

from siriushlacon.epicstel.consts import (
    EPICSTEL_MAIN_UI,
    EPICSTEL_LOGIN_UI,
    EPICSTEL_SERVER,
    EPICSTEL_SERVER_USER,
    EPICSTEL_SERVER_PASS,
    EPICSTEL_LOCATION,
    EPICSTEL_GROUP_UI,
)

logger = logging.getLogger()


class Window(Display, QMainWindow):
    filetypes = {
        "authorized_personnel.csv": "User Groups",
        "groups.csv": "PV Groups",
        "monitor_info.csv": "PV Monitor Information",
    }

    supported_files = (
        "Configuration files (authorized_personnel.csv groups.csv monitor_info.csv)"
    )

    headers = {
        "groups.csv": ["Group", "PVs", "StdMax", "StdMin", "StdTimeout"],
        "monitor_info.csv": [
            "PVNames",
            "PVGroups",
            "ChatIDs",
            "Max",
            "Min",
            "Timeout",
            "DisconnectDate",
            "WarningCount",
        ],
        "authorized_personnel.csv": ["ADM", "TeamADM", "General"],
    }

    new_filetype = None
    config_file = None
    is_remote = False

    def open(self, args):
        if self.keep_changes():
            return

        self.config_file, _ = QFileDialog.getOpenFileName(
            None, "Open", "", self.supported_files
        )

        if self.config_file is not None and self.config_file != "":
            self.display_table()
            self.is_remote = False
            logger.debug("Loaded config file from {}".format(self.config_file))

    def remote_save(self):
        df = pandas.DataFrame.from_dict(self.table.model()._data, orient="columns")
        df.to_csv(self.config_file, header=self.table.model()._header, index=False)
        logger.debug("Loaded and pushed config file from {}".format(self.config_file))

        self.sftp.put(self.config_file, f"{EPICSTEL_LOCATION}{self.config_file[4:]}")

    def save(self, args):
        if self.is_remote:
            login = Login()
            login.accepted.connect(self.remote_save)

            login.show()
        else:
            if self.new_filetype is not None:
                save_file, _ = QFileDialog.getSaveFileName(
                    None, "Save", self.new_filetype, self.supported_files
                )

                if save_file:
                    self.config_file = save_file
                    self.new_filetype = ""
                    self.location_label.setText(self.config_file)

            if self.config_file is not None:
                df = pandas.DataFrame.from_dict(
                    self.table.model()._data, orient="columns"
                )
                df.to_csv(
                    self.config_file, header=self.table.model()._header, index=False
                )

                self.statusBar().showMessage(f"Saved at {self.config_file}")

    def new(self, args):
        if self.keep_changes():
            return

        model = TableModel(
            [["" for i in range(0, len(self.headers[args]))]], self.headers[args]
        )
        self.table.setModel(model)

        self.config_type_label.setText(self.filetypes[args])

        self.save_btn.setEnabled(True)
        self.delete_row_btn.setEnabled(True)
        self.new_row_btn.setEnabled(True)

        self.new_filetype = args
        self.config_file = None

        self.new_usrgp_btn.setEnabled(args == "authorized_personnel.csv")

        self.is_remote = False

    def cell_clicked(self, args):
        if len(self.table.selectedIndexes()) < 1:
            return
        row = self.table.selectedIndexes()[0].row()
        col = self.table.selectedIndexes()[0].column()

        data = self.table.model()._data[row][col]
        pv_data = self.table.model()._data[row][1]

        if type(data) == str and ";" in data:
            c_data = [pv_data.split(";")]
            header = ["PV"]

            if col != 1:
                c_data.append(data.split(";"))
                header.append(self.table.model()._header[col])

            model = PvTableModel(c_data, header, self.table)
            self.pv_table.setModel(model)
            self.pv_table.resizeColumnsToContents()

            self.del_pv_btn.setEnabled(True)
            self.add_pv_btn.setEnabled(True)

    def del_pv(self, args):
        index = self.table.selectedIndexes()[0]
        indexes = self.pv_table.selectedIndexes()

        model = self.pv_table.model()
        parent_model = self.table.model()

        marked_for_deletion = [self.pv_table.model()._data[0][i.row()] for i in indexes]

        for del_pv in marked_for_deletion:
            del_index = model._data[0].index(del_pv)
            model._data[0].pop(del_index)
            model._data[1].pop(del_index)

            for i in range(1, 4):
                vals = parent_model._data[index.row()][i].split(";")
                vals.pop(del_index)
                parent_model._data[index.row()][i] = ";".join(vals)

        model.layoutChanged.emit()
        parent_model.layoutChanged.emit()

    def add_pv(self, args):
        row = self.table.selectedIndexes()[0].row()

        parent_model = self.table.model()
        model = self.pv_table.model()

        model._data[0].append("New PV")
        if len(model._data) > 1:
            model._data[1].append("1")

        parent_model._data[row][1] = parent_model._data[row][1] + ";New Pv"

        for i in range(2, 4):
            parent_model._data[row][i] = parent_model._data[row][i] + ";1"

        parent_model.layoutChanged.emit()
        model.layoutChanged.emit()

    def add_row(self, args):
        data = self.table.model()._data
        new_row = ["" for i in range(0, len(data[0]))]

        data.append(new_row)

        self.table.model().layoutChanged.emit()

    def del_row(self, args):
        indexes = self.table.selectedIndexes()
        marked_for_deletion = [
            self.table.model()._data[index.row()][0] for index in indexes
        ]

        for pv in marked_for_deletion:
            for i in range(0, len(self.table.model()._data)):
                if self.table.model()._data[i][0] == pv:
                    self.table.model()._data.pop(i)
                    break

        self.table.model().layoutChanged.emit()

    def add_usrgp(self, args):
        model = self.table.model()

        for m in model._data:
            m.append("")

        model._header.append("New Group")

        model.layoutChanged.emit()

    def keep_changes(self):
        if self.config_file is not None:
            data = pandas.read_csv(self.config_file).to_dict("split")["data"]

            if self.new_filetype is not None or self.table.model()._data != data:
                reply = QMessageBox.question(
                    self,
                    "Unsaved changes",
                    "You have unsaved changes. Do you wish to continue?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                return reply != QMessageBox.Yes
            else:
                return False
        else:
            return False

    def open_remote(self, file):
        self.transport = paramiko.Transport(EPICSTEL_SERVER)
        logger.info("Fetching from {}".format(EPICSTEL_SERVER))
        logger.info("Logging in...")

        try:
            self.transport.connect(
                username=EPICSTEL_SERVER_USER, password=EPICSTEL_SERVER_PASS
            )  # Root?
        except paramiko.ssh_exception.AuthenticationException:
            QMessageBox.critical(
                self,
                "Could not authenticate",
                "The program could not authenticate itself to the remote servers. You may only edit files locally.",
                QMessageBox.Ok
            )

            logger.error("Could not authenticate to remote server and retrieve files.")
            return

        self.is_remote = True

        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        logger.info("Finalized file transfer!")

        self.config_file = f"/tmp/{file}"
        self.sftp.get(f"{EPICSTEL_LOCATION}{file}", self.config_file)

        self.display_table()

    def edit_header(self, index):
        if self.config_type_label.text() == "User Groups":
            gp_dialog = EditGroup(self.table.model()._header[index])

            gp_dialog.group_edited.connect(
                lambda name: self.table.model().setHeader(index, name)
            )
            gp_dialog.group_deleted.connect(
                lambda name: self.table.model().deleteHeader(index, name)
            )

    def display_table(self):
        self.new_filetype = ""
        data = pandas.read_csv(self.config_file).fillna("").to_dict("split")

        table = data["data"]

        model = TableModel(table, data["columns"])
        self.table.setModel(model)
        self.table.horizontalHeader().sectionClicked.connect(self.edit_header)

        self.save_btn.setEnabled(True)
        self.delete_row_btn.setEnabled(True)
        self.new_row_btn.setEnabled(True)

        config_type = self.filetypes[
            self.config_file[self.config_file.rfind("/") + 1 :]
        ]

        self.location_label.setText("Remote")
        self.config_type_label.setText(config_type)

        self.new_usrgp_btn.setEnabled(config_type == "User Groups")

    def save_on_close(self):
        if self.is_remote or self.config_file is not None:
            data = pandas.read_csv(self.config_file).fillna("").to_dict("split")["data"]
            condition = self.table.model()._data != data
        else:
            condition = self.new_filetype is not None and self.table.model()._data != [
                ["" for i in range(0, len(self.table.model()._header))]
            ]

        if condition:
            reply = QMessageBox.question(
                self,
                "Unsaved changes",
                "You have unsaved changes. Do you wish to save?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.save(0)

    def closeEvent(self, args):
        self.save_on_close()
        # Keeping for possible additions in the future

    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=EPICSTEL_MAIN_UI)

        self.open_config.triggered.connect(self.open)

        self.save_btn.clicked.connect(self.save)
        self.table.clicked.connect(self.cell_clicked)

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        self.add_pv_btn.clicked.connect(self.add_pv)
        self.del_pv_btn.clicked.connect(self.del_pv)

        self.delete_row_btn.clicked.connect(self.del_row)
        self.new_row_btn.clicked.connect(self.add_row)

        self.new_pvgps.triggered.connect(lambda: self.new("groups.csv"))
        self.new_pvinfo.triggered.connect(lambda: self.new("monitor_info.csv"))
        self.new_usrgp.triggered.connect(lambda: self.new("authorized_personnel.csv"))

        self.open_groups.triggered.connect(lambda: self.open_remote("groups.csv"))
        self.open_info.triggered.connect(lambda: self.open_remote("monitor_info.csv"))
        self.open_usr.triggered.connect(
            lambda: self.open_remote("authorized_personnel.csv")
        )

        self.new_usrgp_btn.clicked.connect(self.add_usrgp)

        urllib3.disable_warnings()


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None, macros=None, args=None):
        super(Login, self).__init__()
        uic.loadUi(EPICSTEL_LOGIN_UI, self)
        self.show()

        self.button_box.accepted.connect(self.handle_login)
        self.button_box.rejected.connect(self.destroy)

    def handle_login(self):
        try:
            response = requests.post(
                "https://10.0.38.42/mgmt/bpl/login",
                data={
                    "username": self.username.text(),
                    "password": self.password.text(),
                },
                verify=False,
            )
        except ConnectionError:
            QMessageBox.critical(
                self,
                "Could not authenticate",
                "The program could not connect itself to the remote authentication server.",
                QMessageBox.Ok
            )

            logger.error("Could not connect to authentication server.")

        if "authenticated" in response.text:
            self.accept()
        else:
            QMessageBox.information(
                self,
                "Invalid credentials",
                "Invalid credentials",
                QMessageBox.Ok,
            )
            self.destroy()


class EditGroup(QtWidgets.QDialog):
    group_edited = QtCore.Signal(str)
    group_deleted = QtCore.Signal(str)

    def __init__(self, group, parent=None, macros=None, args=None):
        super(EditGroup, self).__init__()
        uic.loadUi(EPICSTEL_GROUP_UI, self)
        self.show()

        self.group_edit.setText(group)

        self.button_box.accepted.connect(self.handle_edit_group)
        self.button_box.rejected.connect(self.destroy)
        self.delete_btn.clicked.connect(self.handle_delete_group)

    def handle_edit_group(self):
        self.group_edited.emit(self.group_edit.text())

    def handle_delete_group(self):
        self.group_deleted.emit(self.group_edit.text())
        self.destroy()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())