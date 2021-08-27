"""Alter REDIS_HOST to your host's IP"""

import subprocess
from datetime import datetime
from time import localtime, sleep, strftime

from pydm import Display
from qtpy import QtCore, QtGui, QtWidgets, uic
from qtpy.QtGui import QBrush
from qtpy.QtWidgets import QInputDialog
from siriuspy.search import PSSearch

from siriushlacon.beaglebones.BBBread import RedisServer
from siriushlacon.beaglebones.consts import (
    BEAGLEBONES_MAIN,
    BEAGLEBONES_MAIN_UI,
    CHANGE_BBB_UI,
    GREEN_LED,
    INFO_BBB_UI,
    LOGS_BBB_UI,
    RED_LED,
    TABLES,
)

# Corporate test server
# REDIS_HOST = '10.0.6.64'
# Sirius server
REDIS_HOST = "10.0.38.59"

room_names = {
    "All": "",
    "Others": "Outros",
    "TL": "LTs",
    "Connectivity": "Conectividade",
    "Power Supplies": "Fontes",
    "RF": "RF",
}
# "LTs", "Conectividade", "Fontes", "RF", "Outros"
for i in range(20):
    room_names["IA-{:02d}".format(i + 1)] = "Sala{:02d}".format(i + 1)

Ui_MainWindow, QtBaseClass = uic.loadUiType(BEAGLEBONES_MAIN_UI)
Ui_MainWindow_config, QtBaseClass_config = uic.loadUiType(CHANGE_BBB_UI)
Ui_MainWindow_info, QtBaseClass_info = uic.loadUiType(INFO_BBB_UI)
Ui_MainWindow_logs, QtBaseClass_logs = uic.loadUiType(LOGS_BBB_UI)


class UpdateNodesThread(QtCore.QThread):
    finished = QtCore.Signal(tuple)

    def __init__(self, server):
        QtCore.QThread.__init__(self)
        self.server = server

    def __del__(self):
        self.wait()

    def run(self):
        nodes = self.server.list_connected()
        nodes_info = {}

        for node in nodes:
            nodes_info[node] = self.server.get_node(node)

        self.finished.emit((nodes, nodes_info))


class UpdateLogsThread(QtCore.QThread):
    finished = QtCore.Signal(list)

    def __init__(self, server, hostname=None):
        QtCore.QThread.__init__(self)
        self.server = server
        self.hostname = hostname

    def __del__(self):
        self.wait()

    def run(self):
        # If no host name is set, all logs must be retrieved
        logs = self.server.get_logs(self.hostname)
        all_logs = logs if self.hostname else []

        # Iterates through BBB logs
        if not self.hostname:
            for name in logs:
                bbb_logs = []
                bbb_logs = self.server.get_logs(name)
                for _log in bbb_logs:
                    _log.extend(name[4 : name.index(":Logs")].split(":", 1))

                all_logs.extend(bbb_logs)

        # Sorts logs by most recent to least recent
        all_logs = sorted(all_logs, key=lambda x: int(x[0]), reverse=True)

        self.finished.emit(all_logs)


class BBBreadMainWindow(Display, QtWidgets.QWidget, Ui_MainWindow):
    """BeagleBone Black Redis Activity Display"""

    def __init__(self, parent=None, macros=None):
        super().__init__(parent=parent, macros=macros, ui_filename=BEAGLEBONES_MAIN_UI)

        # Configures redis Server
        self.server = RedisServer()
        self.sudo = False

        # Table models
        self.logs_model = TableModel([[]], ["Timestamp", "IP", "BBB", "Occurence"])
        self.logsTable.setModel(self.logs_model)

        self.basic_model = TableModel([[]], ["IP", "BBB", "Role", "State"])
        self.basicTable.setModel(self.basic_model)

        self.advanced_model = TableModel([[]], ["IP", "BBB", "Role", "State"])
        self.advancedTable.setModel(self.advanced_model)

        self.services_model = TableModel([[]], ["IP", "BBB", "Role", "State"])
        self.servicesTable.setModel(self.services_model)

        self.ps_model = TableModel([[]], ["IP", "BBB", "Power Supply", "State"])
        self.psTable.setModel(self.ps_model)

        self.servicesTable.horizontalHeader().setResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )

        self.basicTable.horizontalHeader().setResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )

        self.advancedTable.horizontalHeader().setResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )

        # Lists
        self.nodes = []
        self.nodes_info = {}
        self.data = []

        # List Update Timer
        self.autoUpdate_timer = QtCore.QTimer(self)
        self.autoUpdate_timer.timeout.connect(self.update_nodes)
        self.autoUpdate_timer.setSingleShot(False)
        self.autoUpdate_timer.start(1000)

        # Buttons
        self.basicTable.selectionModel().selectionChanged.connect(self.enable_buttons)
        self.advancedTable.selectionModel().selectionChanged.connect(
            self.enable_buttons
        )
        self.servicesTable.selectionModel().selectionChanged.connect(
            self.enable_buttons
        )
        self.logsTable.selectionModel().selectionChanged.connect(self.enable_buttons)
        self.psTable.selectionModel().selectionChanged.connect(self.enable_buttons)
        self.tabWidget.currentChanged.connect(self.enable_buttons)
        self.deleteButton.clicked.connect(self.delete_nodes)
        self.rebootButton.clicked.connect(self.reboot_nodes)
        self.configButton.clicked.connect(self.config_node)
        self.infoButton.clicked.connect(self.show_node_info)
        self.applyserviceButton.clicked.connect(self.service_application)
        self.logsButton.clicked.connect(self.display_logs)
        self.threadCheckBox.stateChanged.connect(self.update_filters)
        self.commandsCheckBox.stateChanged.connect(self.update_filters)

        # Threading
        self.nodes_thread = UpdateNodesThread(self.server)
        self.nodes_thread.finished.connect(self.update_node_list)
        self.logs_thread = UpdateLogsThread(self.server)
        self.logs_thread.finished.connect(self.update_table)

        # Log Filters
        self.toTimeEdit.dateTimeChanged.connect(self.update_filters)
        self.fromTimeEdit.dateTimeChanged.connect(self.update_filters)
        self.filterEdit.textChanged.connect(self.update_filters)

        # Loads loading indicators
        self.loading_icon = QtGui.QPixmap(RED_LED).scaledToHeight(20)
        self.idle_icon = QtGui.QPixmap(GREEN_LED).scaledToHeight(20)

        # State lock
        self.updating = False
        self.fetch_ps = True

    def update_nodes(self):
        """Updates list of BBBs shown"""
        # Stores every BBB information
        self.status_icon.setPixmap(self.loading_icon)
        if not self.nodes_thread.isRunning():
            self.nodes_thread.start()

        # Updates logs
        if not self.logs_thread.isRunning():
            self.logs_thread.start()

    def update_filters(self):
        """Updates tables with filters set by user"""
        if not self.data:
            return

        search = self.filterEdit.text()

        if self.tabWidget.currentIndex() == 4:
            max_date = self.toTimeEdit.dateTime().toPyDateTime().timestamp()
            min_date = self.fromTimeEdit.dateTime().toPyDateTime().timestamp()

            if min_date > max_date:
                self.fromTimeEdit.setDateTime(self.toTimeEdit.dateTime())

            if min_date == max_date:
                self.update_table(self.data)

            length = len(self.data)
            min_index, max_index = length, 0

            # Compares Unix timestamp for logs and filter, stops when a log satisfies the filter
            for index, log in enumerate(self.data):
                if int(log[0]) < min_date:
                    min_index = index
                    break

            for index, log in enumerate(self.data[::-1]):
                if int(log[0]) > max_date:
                    max_index = length - index
                    break

            data = self.data[max_index:min_index]

            if search:
                data = [r for r in data if search in r[3] or search in r[2]]

            self.update_table(data, update=False)
            return True
        elif self.tabWidget.currentIndex() == 3:
            data = {}
            if not self.fetch_ps:
                return False
            for node in self.nodes_info:
                self.nodes_info[node]["ps"] = []
                try:
                    for ps in PSSearch.conv_bbbname_2_psnames(
                        self.nodes_info[node][b"name"].decode().replace("--", ":")
                    ):
                        if search in node or search in ps[0]:
                            self.nodes_info[node]["ps"].append(ps[0])
                            data[node] = self.nodes_info[node]
                except KeyError:
                    continue
                except Exception as e:
                    if "could not" in str(e):
                        self.fetch_ps = False
                        QtWidgets.QMessageBox.question(
                            self,
                            "Error",
                            "Could not connect to control system constants server. Please set the SIRIUS_URL_CONSTS environment variable to a valid server.",
                            QtWidgets.QMessageBox.Ok,
                        )
                    return

            self.update_node_list(data, update=False)
        else:
            data = {}
            for key in self.nodes_info:
                if search in key or search in key.replace("--", ":"):
                    data[key] = self.nodes_info[key]
            self.update_node_list(data, update=False)

    def update_table(self, logs, update=True):
        """Updates content of logs table"""
        if update:
            self.data = logs
            self.update_filters()
            return

        # Formats timestamp in human readable form
        data = [
            [
                datetime.utcfromtimestamp(int(_log[0])).strftime("%d/%m/%Y %H:%M:%S"),
                _log[2],
                _log[3].replace("--", ":"),
                _log[1],
            ]
            for _log in logs
        ]

        # Filters out thread statuses and commands (if boxes aren't checked)
        if self.threadCheckBox.isChecked():
            if not self.commandsCheckBox.isChecked():
                data = [
                    _log
                    for _log in data
                    if "connected" in _log[2].lower()
                    or "hostname" in _log[2].lower()
                    or "thread found an exception" in _log[2].lower()
                    or "thread died" in _log[2].lower()
                ]
        else:
            if not self.commandsCheckBox.isChecked():
                data = [
                    _log
                    for _log in data
                    if "connected" in _log[2].lower() or "hostname" in _log[2].lower()
                ]
            else:
                data = [
                    _log
                    for _log in data
                    if "thread found an exception" not in _log[2].lower()
                    and "thread died" not in _log[2].lower()
                ]

        self.logs_model.set_data(data)

        self.status_icon.setPixmap(self.idle_icon)

    def update_node_list(self, nodes, update=True):  # noqa: C901
        """Gets updated node list and applies it to all lists"""
        if update:
            self.nodes, self.nodes_info = nodes
            self.update_filters()
            return

        names = nodes.keys()
        node_info = nodes
        data = []
        connected_number = 0

        current_tab = self.tabWidget.currentIndex()
        if current_tab == 4:
            return

        if current_tab == 1:
            state_filter = {
                "Connected": self.connectedAdvancedBox.isChecked(),
                "Disconnected": self.disconnectedAdvancedBox.isChecked(),
                "Moved": self.movedAdvancedBox.isChecked(),
            }
        elif current_tab == 0:
            state_filter = {
                "Connected": self.connectedCheckBox.isChecked(),
                "Disconnected": self.disconnectedCheckBox.isChecked(),
                "Moved": self.movedCheckBox.isChecked(),
            }
        elif current_tab == 3:
            state_filter = {"Connected": True, "Disconnected": True, "Moved": True}
        else:
            state_filter = {"Connected": True, "Disconnected": False, "Moved": False}

        list_name = getattr(self, TABLES[current_tab] + "_model")

        # Advanced Tab filters
        ip_filter = {
            "manual": self.staticipAdvancedBox.isChecked(),
            "dhcp": self.dhcpAdvancedBox.isChecked(),
            "Undefined": self.undeterminedAdvancedBox.isChecked(),
            "StaticIP": self.staticipAdvancedBox.isChecked(),
        }
        equipment_filter = {
            "MKS": self.mksAdvancedBox.isChecked(),
            "4UHV": self.uhvAdvancedBox.isChecked(),
            "MBTEMP": self.mbtempAdvancedBox.isChecked(),
            "THERMO": self.thermoAdvancedBox.isChecked(),
            "COUNTING": self.countingpruAdvancedBox.isChecked(),
            "POWER": self.powersupplyAdvancedBox.isChecked(),
            "SPIXCONV": self.spixconvAdvancedBox.isChecked(),
            "SIMAR": self.simarAdvancedBox.isChecked(),
            "Searching": self.nodevAdvancedBox.isChecked(),
            "": self.nodevAdvancedBox.isChecked(),
        }

        self.updating = True
        for node, info in node_info.items():
            if node not in names:
                continue
            try:
                # Organizes node information
                node_ip = info[b"ip_address"].decode()
                node_ip_type = info[b"ip_type"].decode()
                node_name = info[b"name"].decode()
                node_sector = info[b"sector"].decode()
                node_state = info[b"state_string"].decode()
                node_details = info[b"details"].decode()
                node_importance = (
                    info.get(b"matching_bbb").decode().capitalize()
                    if info.get(b"matching_bbb")
                    else "Primary"
                )
            except Exception:
                continue
            # Filters by name and displays node in list
            if room_names[self.roomBox.currentText()] in [node_sector, ""]:
                if node_state[:3] == "BBB":
                    node_state = "Moved"

                if current_tab == 3:
                    if node_state == "Connected":
                        connected_number += 1
                    for ps in info["ps"]:
                        data.append(
                            [node_ip, node_name.replace("--", ":"), ps, node_state]
                        )
                else:
                    for equipment, efilter in equipment_filter.items():
                        # Filters by equipment if advanced tab is selected
                        if (
                            equipment in node_details
                            and efilter
                            and node_ip_type != "0.0.0.0"
                            and (ip_filter[node_ip_type] or ip_filter["Undefined"])
                        ) or current_tab != 1:
                            if state_filter[node_state]:
                                data.append(
                                    [
                                        node_ip,
                                        node_name.replace("--", ":"),
                                        node_importance,
                                        node_state,
                                    ]
                                )
                            break

        list_name.set_data(data)
        self.updating = False
        # Updates the number of connected and listed nodes
        if current_tab == 3:
            self.connectedLabel.setText("Listed PS nodes: {}".format(connected_number))
            self.listedLabel.setText("")
        elif current_tab == 4:
            self.connectedLabel.setText("")
            self.listedLabel.setText("")
        else:
            self.connectedLabel.setText(
                "Connected nodes: {}".format(
                    sum(
                        self.nodes_info[n][b"state_string"].decode() == "Connected"
                        for n in self.nodes_info
                    )
                )
            )
            self.listedLabel.setText("Listed: {}".format(list_name.rowCount()))
        self.status_icon.setPixmap(self.idle_icon)

    @staticmethod
    def remove_faulty(node_string, list_name: QtWidgets.QListWidget, all_elements=True):
        """Removes duplicates and nodes that shouldn't be on the list"""
        qlistitem = list_name.findItems(node_string, QtCore.Qt.MatchExactly)
        if qlistitem:
            if all_elements:
                for node in qlistitem:
                    list_name.takeItem(list_name.row(node))
            elif len(qlistitem) > 1:
                qlistitem.reverse()
                list_name.takeItem(list_name.row(qlistitem[0]))

    def enable_buttons(self):
        """Enables Buttons when one or more boards are selected"""
        current_tab = self.tabWidget.currentIndex()
        selected_items = (
            getattr(self, TABLES[current_tab] + "Table").selectionModel().selectedRows()
        )

        if selected_items:
            self.rebootButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

            is_single = len(selected_items) == 1
            self.configButton.setEnabled(is_single)
            self.infoButton.setEnabled(is_single)
            self.logsButton.setEnabled(is_single)

            self.applyserviceButton.setEnabled(current_tab == 2)
        else:
            self.logsButton.setEnabled(False)
            self.rebootButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.configButton.setEnabled(False)
            self.infoButton.setEnabled(False)
            self.applyserviceButton.setEnabled(False)

    def reboot_nodes(self):
        """Reboots the selected nodes"""
        if not self.sudo:
            text, confirmation = QInputDialog.getText(
                self,
                "Confirmation",
                (
                    "Rebooting could result in downtime, failures or worse, and whoever"
                    "\nexecutes this should be aware of the implications of this action.\n"
                    "\nIf you want to enter sudo mode, type in 'Beaglebone' (case sensitive)"
                ),
            )
            if confirmation and text == "Beaglebone":
                self.sudo = True
            else:
                return

        confirmation = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to reboot these nodes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirmation == QtWidgets.QMessageBox.Yes:
            current_tab = self.tabWidget.currentIndex()
            selected_items = (
                getattr(self, TABLES[current_tab] + "Table")
                .selectionModel()
                .selectedRows()
            )

            for bbb in selected_items:
                bbb_ip = bbb.sibling(bbb.row(), 0 if current_tab != 4 else 1).data()
                bbb_hostname = (
                    bbb.sibling(bbb.row(), 1 if current_tab != 4 else 2)
                    .data()
                    .replace(":", "--")
                )
                self.server.reboot_node(bbb_ip, bbb_hostname)

    def delete_nodes(self):
        """Deletes hashs from Redis Database"""
        confirmation = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure about deleting these nodes from Redis Database?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirmation == QtWidgets.QMessageBox.Yes:
            current_tab = self.tabWidget.currentIndex()
            selected_items = (
                getattr(self, TABLES[current_tab] + "Table")
                .selectionModel()
                .selectedRows()
            )

            errors = []
            for bbb in selected_items:
                bbb_ip = bbb.sibling(bbb.row(), 0 if current_tab != 4 else 1).data()
                bbb_hostname = (
                    bbb.sibling(bbb.row(), 1 if current_tab != 4 else 2)
                    .data()
                    .replace(":", "--")
                )

                bbb_hashname = "BBB:{}:{}".format(bbb_ip, bbb_hostname)
                try:
                    self.server.delete_bbb(bbb_hashname)
                    while self.updating:
                        sleep(0.1)
                    self.nodes_info.pop(bbb_hashname)
                    self.update_nodes()

                except KeyError:
                    errors.append(bbb_hashname)
                    continue
            if errors:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Warning",
                    "The following nodes weren't found in the Redis Database:\n{}".format(
                        "\n".join(errors)
                    ),
                    QtWidgets.QMessageBox.Abort,
                )

    def display_logs(self):
        """Shows selected BBB's logs"""
        current_tab = self.tabWidget.currentIndex()

        index = (
            getattr(self, TABLES[current_tab] + "Table")
            .selectionModel()
            .selectedRows()[0]
        )

        bbb_ip = index.sibling(index.row(), 0 if current_tab != 4 else 1).data()
        bbb_hostname = (
            index.sibling(index.row(), 1 if current_tab != 4 else 2)
            .data()
            .replace(":", "--")
        )

        hashname = "BBB:{}:{}:Logs".format(bbb_ip, bbb_hostname)
        try:
            self.window = BBBLogs(self.server, hashname)
            self.window.show()
        except KeyError:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "The node you are trying to get information isn't connected",
                QtWidgets.QMessageBox.Abort,
            )

    def show_node_info(self):
        """Shows selected BBB's information"""
        current_tab = self.tabWidget.currentIndex()
        index = (
            getattr(self, TABLES[current_tab] + "Table")
            .selectionModel()
            .selectedRows()[0]
        )
        bbb_ip = index.sibling(index.row(), 0 if current_tab != 4 else 1).data()
        bbb_hostname = (
            index.sibling(index.row(), 1 if current_tab != 4 else 2)
            .data()
            .replace(":", "--")
        )

        hashname = "BBB:{}:{}".format(bbb_ip, bbb_hostname)
        try:
            info = self.nodes_info[hashname]
            self.window = BBBInfo(info)
            self.window.show()
        except KeyError:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "The node you are trying to get information isn't connected",
                QtWidgets.QMessageBox.Abort,
            )

    def config_node(self):
        """Opens configuration the selected BBB's configuration window"""
        current_tab = self.tabWidget.currentIndex()
        index = (
            getattr(self, TABLES[current_tab] + "Table")
            .selectionModel()
            .selectedRows()[0]
        )

        bbb_ip = index.sibling(index.row(), 0 if current_tab != 4 else 1).data()
        bbb_hostname = (
            index.sibling(index.row(), 1 if current_tab != 4 else 2)
            .data()
            .replace(":", "--")
        )

        hashname = "BBB:{}:{}".format(bbb_ip, bbb_hostname)
        info = self.nodes_info[hashname]
        if info[b"state_string"].decode() == "Connected":
            if not self.sudo:
                text, confirmation = QInputDialog.getText(
                    self,
                    "Confirmation",
                    (
                        "This interface is meant for advanced changes that could result in downtime,"
                        "\nfailures or worse.\n"
                        "\nIf you want to enter sudo mode, type in 'Beaglebone' (case sensitive)"
                    ),
                )
                if confirmation and text == "Beaglebone":
                    self.sudo = True

            if self.sudo:
                self.window = BBBConfig(hashname, info, self.server)
                self.window.show()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "The node you are trying to configure isn't connected",
                QtWidgets.QMessageBox.Abort,
            )

    def service_application(self):
        """Applies services modification"""
        confirmation = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to apply these changes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirmation == QtWidgets.QMessageBox.Yes:
            index = self.servicesTable.selectionModel().selectedRows()[0]

            selected_operation = self.operationcomboBox.currentText()
            if selected_operation == "Restart":
                operation = self.server.restart_service
            else:
                operation = self.server.stop_service
            selected_bbbs = self.servicesTable.selectionModel().selectedRows()
            for bbb in selected_bbbs:
                bbb_ip = index.sibling(bbb.row(), 0)
                bbb_hostname = index.sibling(bbb.row(), 1)
                if self.bbbreadBox.isChecked():
                    operation(bbb_ip, "bbbread", bbb_hostname)
                if self.bbbfunctionBox.isChecked():
                    operation(bbb_ip, "bbb-function", bbb_hostname)
                if self.ethbridgeBox.isChecked():
                    operation(bbb_ip, "eth-bridge-pru-serial485", bbb_hostname)
                if self.simarBox.isChecked():
                    operation(bbb_ip, "simar_sensors", bbb_hostname)


class BBBInfo(QtWidgets.QWidget, Ui_MainWindow_info):
    """BBB info display"""

    def __init__(self, info):
        QtWidgets.QWidget.__init__(self)
        Ui_MainWindow_info.__init__(self)
        self.setupUi(self)

        if info:
            node_ip = info[b"ip_address"].decode()
            node_ip_type = info[b"ip_type"].decode()
            node_name = info[b"name"].decode()
            node_sector = info[b"sector"].decode()
            ping_time = float(info[b"ping_time"].decode())
            for room, number in room_names.items():
                if number == node_sector:
                    node_sector = room
                    break
            node_state = info[b"state_string"].decode()
            node_details = info[b"details"].decode()
            node_config_time = info[b"config_time"].decode()
            nameservers = info[b"nameservers"].decode()
            self.nameLabel.setText(node_name)
            self.ipLabel.setText(node_ip)
            self.stateLabel.setText(node_state)
            self.iptypeLabel.setText(node_ip_type)
            self.configtimevalueLabel.setText(node_config_time)
            self.equipmentvalueLabel.setText(node_details)
            self.nameserversvalueLabel.setText(nameservers)
            self.sectorvalueLabel.setText(node_sector)
            self.lastseenvalueLabel.setText(
                strftime("%a, %d %b %Y   %H:%M:%S", localtime(ping_time))
            )


class TableModel(QtCore.QAbstractTableModel):
    """Display model for TableView"""

    def __init__(self, data, header):
        super(TableModel, self).__init__()
        self._data = data
        self._header = header

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._header[section]

    def data(self, index, role):
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            return self._data[index.row()][index.column()]
        if role == QtCore.Qt.BackgroundRole:
            if self.columnCount() < 3 or self._data[index.row()][2] == "Connected":
                return QBrush(QtCore.Qt.white)
            if self._data[index.row()][3] == "Disconnected":
                return QBrush(QtCore.Qt.red)
            if self._data[index.row()][3] == "Moved":
                return QBrush(QtCore.Qt.yellow)

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
        self.layoutChanged.emit()

    def rowCount(self, _=None):
        return len(self._data)

    def columnCount(self, _=None):
        if self.rowCount(0) < 1:
            return 0
        return len(self._data[0])


class BBBLogs(QtWidgets.QWidget, Ui_MainWindow_logs):
    # BBB Logs Display
    def __init__(self, server, hashname):
        QtWidgets.QWidget.__init__(self)
        Ui_MainWindow_logs.__init__(self)
        self.setupUi(self)
        self.data = []

        self.logs_thread = UpdateLogsThread(server, hashname)
        self.logs_thread.finished.connect(self.update_table)

        self.model = TableModel([[]], ["Timestamp", "Occurence"])
        self.logsTable.setModel(self.model)

        self.fromTimeEdit.dateTimeChanged.connect(self.update_filters)
        self.toTimeEdit.dateTimeChanged.connect(self.update_filters)

        self.filterEdit.textChanged.connect(self.update_filters)

        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.logs_thread.start)
        self.update_timer.setSingleShot(False)
        self.update_timer.start(1000)

    def update_table(self, logs, update=True):
        """Sets table values and converts timestamp, deep copies logs"""
        if update:
            self.data = logs
            self.update_filters()
            return

        data = [
            [
                datetime.utcfromtimestamp(int(_log[0])).strftime("%d/%m/%Y %H:%M:%S"),
                _log[1],
            ]
            for _log in logs
        ]

        self.model.set_data(data)

    def update_filters(self):
        """Updates log table with filters set by user"""
        if not self.data:
            return

        search = self.filterEdit.text()

        max_date = self.toTimeEdit.dateTime().toPyDateTime().timestamp()
        min_date = self.fromTimeEdit.dateTime().toPyDateTime().timestamp()

        if min_date > max_date:
            self.fromTimeEdit.setDateTime(self.toTimeEdit.dateTime())

        if min_date == max_date:
            self.update_table(self.data)

        length = len(self.data)
        min_index, max_index = length, 0

        # Compares Unix timestamp for logs and filter, stops when a log satisfies the filter
        for index, log in enumerate(self.data):
            if int(log[0]) < min_date:
                min_index = index
                break

        for index, log in enumerate(self.data[::-1]):
            if int(log[0]) > max_date:
                max_index = length - index
                break

        data = self.data[max_index:min_index]

        # If the user has set a string filter, all logs without a mention of the filter are removed
        if search:
            data = [r for r in data if search in r[1]]

        self.update_table(data, update=False)


class BBBConfig(QtWidgets.QWidget, Ui_MainWindow_config):
    """BBB configuration display"""

    def __init__(self, hashname, info, server):
        QtWidgets.QWidget.__init__(self)
        Ui_MainWindow_config.__init__(self)
        self.setupUi(self)

        self.server = server

        self.hashname = hashname
        self.hostname = info[b"name"].decode()
        self.ip_address = info[b"ip_address"].decode()
        ip = self.ip_address.split(".")
        self.ip_suffix = ip[-1]
        self.bbb_sector = info[b"sector"].decode()

        self.currenthostnamevalueLabel.setText(self.hostname)
        self.currentipvalueLabel.setText(self.ip_address)

        self.ip_prefix = ".".join(ip[:-1]) + "."

        if ip[1] != "128":
            self.ipComboBox.setEnabled(False)
            self.newipSpinBox.setEnabled(False)
            self.nameserver1Edit.setEnabled(False)
            self.nameserver2Edit.setEnabled(False)
            self.keepipBox.setChecked(True)
            self.keepipBox.setEnabled(False)
            self.keepnameserversBox.setChecked(True)
            self.keepnameserversBox.setEnabled(False)

        self.newipLabel.setText(self.ip_prefix)
        self.ipComboBox.currentIndexChanged.connect(self.disable_spinbox)

        self.applyButton.clicked.connect(self.apply_changes)

    def disable_spinbox(self):
        if self.ipComboBox.currentText() == "MANUAL":
            self.newipSpinBox.setEnabled(True)
        else:
            self.newipSpinBox.setEnabled(False)

    def apply_changes(self):
        # Before asking for confirmation annotates configuration parameters in order to prevent delay bugs
        self.applyButton.setEnabled(False)
        hostname_changed = False
        # DNS
        keep_dns = self.keepnameserversBox.isChecked()
        nameserver_1 = self.nameserver1Edit.text()
        nameserver_2 = self.nameserver2Edit.text()

        # Hostname
        keep_hostname = self.keephostnameBox.isChecked()
        new_hostname = self.hostnameEdit.text()

        # IP
        keep_ip = self.keepipBox.isChecked()
        ip_type = self.ipComboBox.currentText()
        new_ip_suffix = str(self.newipSpinBox.value())

        # Bools to verify if command was sent successfully
        ip_sent = False

        # Confirmation screen
        confirmation = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Apply changes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirmation == QtWidgets.QMessageBox.Yes:
            # Nameservers configuration
            if not keep_dns and nameserver_1 and nameserver_2:
                dns_sent = self.server.change_nameservers(
                    self.ip_address, nameserver_1, nameserver_2, self.hostname
                )
            else:
                dns_sent = True
            # Hostname configuration
            if not keep_hostname and new_hostname:
                name_sent = self.server.change_hostname(
                    self.ip_address, new_hostname, self.hostname
                )
                hostname_changed = name_sent
            else:
                name_sent = True
            if not keep_ip:
                if ip_type in ["DHCP", "dhcp"]:
                    if hostname_changed and name_sent:
                        ip_sent = self.server.change_ip(
                            self.ip_address, "dhcp", self.hostname, override=True
                        )
                        self.hostname = new_hostname
                    else:
                        ip_sent = self.server.change_ip(
                            self.ip_address, "dhcp", self.hostname
                        )
                elif new_ip_suffix not in [self.ip_suffix, "0", "1", "2"]:
                    new_ip = self.ip_prefix + new_ip_suffix
                    if hostname_changed and name_sent:
                        ip_sent = self.server.change_ip(
                            self.ip_address,
                            "manual",
                            self.hostname,
                            new_ip,
                            "255.255.255.0",
                            self.ip_prefix + "1",
                            override=True,
                        )
                        self.hostname = new_hostname
                    else:
                        ip_sent = self.server.change_ip(
                            self.ip_address,
                            "manual",
                            self.hostname,
                            new_ip,
                            "255.255.255.0",
                            self.ip_prefix + "1",
                        )
            else:
                ip_sent = True
            if ip_sent and dns_sent and name_sent:
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    "Node configured successfully",
                    QtWidgets.QMessageBox.Close,
                )
            if not name_sent:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "Error in Hostname configuration",
                    QtWidgets.QMessageBox.Abort,
                )
            if not dns_sent:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "Error in Nameservers configuration",
                    QtWidgets.QMessageBox.Abort,
                )
            if not ip_sent:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    "Error in IP configuration",
                    QtWidgets.QMessageBox.Abort,
                )
            self.close()
        else:
            self.applyButton.setEnabled(True)


if __name__ == "__main__":
    subprocess.Popen("pydm --hide-nav-bar " + BEAGLEBONES_MAIN, shell=True)
