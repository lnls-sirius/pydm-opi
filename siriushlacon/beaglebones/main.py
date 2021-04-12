"""Alter REDIS_HOST to your host's IP"""

import subprocess
from datetime import datetime
from time import sleep, localtime, strftime
from qtpy import QtCore, QtGui, QtWidgets, uic

from pydm import Display
from siriushlacon.beaglebones.BBBread import RedisServer
from siriushlacon.beaglebones.consts import (
    BEAGLEBONES_MAIN_UI,
    BEAGLEBONES_MAIN,
    INFO_BBB_UI,
    CHANGE_BBB_UI,
    LOGS_BBB_UI,
    RED_LED,
    GREEN_LED,
)

qtCreatorFile = BEAGLEBONES_MAIN_UI
qtCreator_configfile = CHANGE_BBB_UI
qtCreator_infofile = INFO_BBB_UI
qtCreator_logsfile = LOGS_BBB_UI

BASIC_TAB = 0
ADVANCED_TAB = 1
SERVICE_TAB = 2
LOGS_TAB = 3
# Corporate test server
# REDIS_HOST = '10.0.6.64'
# Sirius server
REDIS_HOST = "10.128.255.3"

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

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
Ui_MainWindow_config, QtBaseClass_config = uic.loadUiType(qtCreator_configfile)
Ui_MainWindow_info, QtBaseClass_info = uic.loadUiType(qtCreator_infofile)
Ui_MainWindow_logs, QtBaseClass_logs = uic.loadUiType(qtCreator_logsfile)


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
                    _log.insert(1, name[4 : name.index(":Logs")])

                all_logs.extend(bbb_logs)

            # Sorts logs by most recent to least recent
            all_logs = sorted(all_logs, key=lambda x: int(x[0]), reverse=True)

        self.finished.emit(all_logs)


class BBBreadMainWindow(Display, QtWidgets.QWidget, Ui_MainWindow):
    """BeagleBone Black Redis Activity Display"""

    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=BEAGLEBONES_MAIN_UI)

        # Configures redis Server
        self.server = RedisServer()

        # Table models
        self.logs_model = TableModel([[]], all=True)
        self.logsTable.setModel(self.logs_model)

        # Lists
        self.nodes = []
        self.nodes_info = {}
        self.data = None
        self.basicList.setSortingEnabled(True)
        self.basicList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.advancedList.setSortingEnabled(True)
        self.advancedList.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.serviceList.setSortingEnabled(True)
        self.serviceList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # List Update Timer
        self.autoUpdate_timer = QtCore.QTimer(self)
        self.autoUpdate_timer.timeout.connect(self.update_nodes)
        self.autoUpdate_timer.setSingleShot(False)
        self.autoUpdate_timer.start(1000)

        # Buttons
        self.basicList.itemSelectionChanged.connect(self.enable_buttons)
        self.advancedList.itemSelectionChanged.connect(self.enable_buttons)
        self.serviceList.itemSelectionChanged.connect(self.enable_buttons)
        self.logsTable.selectionModel().selectionChanged.connect(self.enable_buttons)
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
        self.filterEdit.textChanged.connect(self.update_log_text)

        # Loads loading indicators
        self.loading_icon = QtGui.QPixmap(RED_LED).scaledToHeight(20)
        self.idle_icon = QtGui.QPixmap(GREEN_LED).scaledToHeight(20)

    def update_nodes(self):
        """Updates list of BBBs shown"""
        # Stores every BBB information
        self.status_icon.setPixmap(self.loading_icon)
        if not self.nodes_thread.isRunning():
            self.nodes_thread.start()

        # Updates logs
        if not self.logs_thread.isRunning():
            self.logs_thread.start()

    def update_log_text(self):
        """ Sets table values and converts timestamp, deep copies logs """
        if self.tabWidget.currentIndex() == LOGS_TAB:
            self.update_filters()

    def update_filters(self):
        """ Updates log table with filters set by user """
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
        for index, r in enumerate(self.data):
            if int(r[0]) < min_date:
                min_index = index
                break

        for index, r in enumerate(self.data[::-1]):
            if int(r[0]) > max_date:
                max_index = length - index
                break

        data = self.data[max_index:min_index]

        # If the user has set a string filter, all logs without a mention of the filter are removed
        if search:
            data = [r for r in data if search in r[2] or search in r[1]]

        self.update_table(data, update=False)

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
                _log[1],
                _log[2],
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
                    or "thread died" in _log[2].lower()
                ]
        else:
            if not self.commandsCheckBox.isChecked():
                data = [
                    _log
                    for _log in data
                    if "connected" in _log[2].lower() or "hostname" in _log[2].lower()
                ]
            data = [_log for _log in data if "thread died" not in _log[2].lower()]

        self.logs_model.set_data(data)

    def update_node_list(self, nodes):  # noqa: C901
        """Gets updated node list and applies it to all lists"""
        self.nodes, self.nodes_info = nodes
        connected_number = 0

        current_tab = self.tabWidget.currentIndex()
        if current_tab == LOGS_TAB:
            self.connectedLabel.hide()
            self.listedLabel.hide()
        else:
            self.connectedLabel.show()
            self.listedLabel.show()

        if current_tab == ADVANCED_TAB:
            state_filter = {
                "Connected": self.connectedAdvancedBox.isChecked(),
                "Disconnected": self.disconnectedAdvancedBox.isChecked(),
                "Moved": self.movedAdvancedBox.isChecked(),
            }
            list_name = self.advancedList
        elif current_tab == BASIC_TAB:
            state_filter = {
                "Connected": self.connectedCheckBox.isChecked(),
                "Disconnected": self.disconnectedCheckBox.isChecked(),
                "Moved": self.movedCheckBox.isChecked(),
            }
            list_name = self.basicList
        else:
            state_filter = {"Connected": True, "Disconnected": False, "Moved": False}
            list_name = self.serviceList

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
            "RACK_MON": self.rackmonitorAdvancedBox.isChecked(),
            "Searching": self.nodevAdvancedBox.isChecked(),
            "": self.nodevAdvancedBox.isChecked(),
        }
        self.Lock = True
        for node, info in self.nodes_info.items():
            if node not in self.nodes:
                continue
            try:
                # Organizes node information
                node_ip = info[b"ip_address"].decode()
                node_ip_type = info[b"ip_type"].decode()
                node_name = info[b"name"].decode()
                node_sector = info[b"sector"].decode()
                node_state = info[b"state_string"].decode()
                node_details = info[b"details"].decode()
                node_string = "{} - {}".format(node_ip, node_name)
            except Exception:
                # print(e)
                continue
            # Increments Connected Number of BBBs if beagle is connected
            if node_state == "Connected":
                connected_number += 1
            # Filters by name and displays node in list
            if (
                self.filterEdit.text() == "" or self.filterEdit.text() in node_string
            ) and room_names[self.roomBox.currentText()] in [node_sector, ""]:
                item = QtWidgets.QListWidgetItem(node_string)
                equipment_len = len(equipment_filter)
                current_equipment = 0
                for equipment, efilter in equipment_filter.items():
                    current_equipment += 1
                    # Filters by equipment if advanced tab is selected
                    if (
                        equipment in node_details
                        and efilter
                        and (ip_filter[node_ip_type] or ip_filter["Undefined"])
                    ) or current_tab in [BASIC_TAB, SERVICE_TAB]:

                        # Filters by node state
                        if node_state == "Connected":
                            if state_filter[node_state]:
                                # Verifies if the node is already on the list
                                qlistitem = list_name.findItems(
                                    node_string, QtCore.Qt.MatchExactly
                                )
                                if not qlistitem:
                                    list_name.addItem(item)
                                    item_index = list_name.row(item)
                                else:
                                    self.remove_faulty(node_string, list_name, False)
                                    item_index = list_name.row(qlistitem[0])
                                # Sets background color as white
                                list_name.item(item_index).setBackground(
                                    QtGui.QColor("white")
                                )
                            else:
                                self.remove_faulty(node_string, list_name)

                        # Disconnected nodes have red background
                        elif node_state == "Disconnected":
                            if state_filter[node_state]:
                                # Verifies if the node is already on the list
                                qlistitem = list_name.findItems(
                                    node_string, QtCore.Qt.MatchExactly
                                )
                                if not qlistitem:
                                    list_name.addItem(item)
                                    item_index = list_name.row(item)
                                else:
                                    self.remove_faulty(node_string, list_name, False)
                                    item_index = list_name.row(qlistitem[0])
                                # Sets background color as red
                                list_name.item(item_index).setBackground(
                                    QtGui.QColor("red")
                                )

                            else:
                                self.remove_faulty(node_string, list_name)

                        # Moved nodes have yellow background
                        elif node_state[:3] == "BBB":
                            # print(node_name)
                            if state_filter["Moved"]:
                                # Verifies if the node is already on the list
                                qlistitem = list_name.findItems(
                                    node_string, QtCore.Qt.MatchExactly
                                )
                                if not qlistitem:
                                    list_name.addItem(item)
                                    item_index = list_name.row(item)
                                else:
                                    self.remove_faulty(node_string, list_name, False)
                                    item_index = list_name.row(qlistitem[0])
                                # Sets background color as yellow
                                list_name.item(item_index).setBackground(
                                    QtGui.QColor("yellow")
                                )
                            else:
                                self.remove_faulty(node_string, list_name)
                        break

                    # If not in any of the selected equipments, removes node
                    if current_equipment == equipment_len:
                        self.remove_faulty(node_string, list_name)

                # Removing duplicates
                self.remove_faulty(node_string, list_name, False)

            else:
                self.remove_faulty(node_string, list_name)
        self.Lock = False
        # Updates the number of connected and listed nodes
        self.connectedLabel.setText("Connected nodes: {}".format(connected_number))
        self.listedLabel.setText("Listed: {}".format(list_name.count()))
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
        if current_tab == BASIC_TAB:
            selected_items = self.basicList.selectedItems()
        elif current_tab == ADVANCED_TAB:
            selected_items = self.advancedList.selectedItems()
        elif current_tab == SERVICE_TAB:
            selected_items = self.serviceList.selectedItems()
        else:
            selected_items = self.logsTable.selectionModel().selectedRows()
        if selected_items:
            self.rebootButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
            if len(selected_items) == 1:
                self.configButton.setEnabled(True)
                self.infoButton.setEnabled(True)
                self.logsButton.setEnabled(True)
            else:
                self.configButton.setEnabled(False)
                self.infoButton.setEnabled(False)
                self.logsButton.setEnabled(False)
            if current_tab == SERVICE_TAB:
                self.applyserviceButton.setEnabled(True)
            else:
                self.applyserviceButton.setEnabled(False)
        else:
            self.logsButton.setEnabled(False)
            self.rebootButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.configButton.setEnabled(False)
            self.infoButton.setEnabled(False)
            self.applyserviceButton.setEnabled(False)

    def reboot_nodes(self):
        """Reboots the selected nodes"""
        confirmation = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure about rebooting these nodes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirmation == QtWidgets.QMessageBox.Yes:
            current_list = self.tabWidget.currentIndex()
            if current_list == BASIC_TAB:
                selected_bbbs = self.basicList.selectedItems()
            elif current_list == ADVANCED_TAB:
                selected_bbbs = self.advancedList.selectedItems()
            elif current_list == SERVICE_TAB:
                selected_bbbs = self.serviceList.selectedItems()
            else:
                selected_bbbs = self.logsTable.selectionModel().selectedRows()
            for bbb in selected_bbbs:
                if current_list == LOGS_TAB:
                    bbb_ip, bbb_hostname = bbb.sibling(bbb.row(), 1).data().split(":")
                else:
                    bbb_ip, bbb_hostname = bbb.text().split(" - ")
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
            current_index = self.tabWidget.currentIndex()
            if current_index == BASIC_TAB:
                selected_bbbs = self.basicList.selectedItems()
            elif current_index == ADVANCED_TAB:
                selected_bbbs = self.advancedList.selectedItems()
            elif current_index == SERVICE_TAB:
                selected_bbbs = self.serviceList.selectedItems()
            else:
                selected_bbbs = self.logsTable.selectionModel().selectedRows()
            errors = []
            for bbb in selected_bbbs:
                if current_index == LOGS_TAB:
                    bbb_ip, bbb_hostname = bbb.sibling(bbb.row(), 1).data().split(":")
                else:
                    bbb_ip, bbb_hostname = bbb.text().split(" - ")
                bbb_hashname = "BBB:{}:{}".format(bbb_ip, bbb_hostname)
                try:
                    self.server.delete_bbb(bbb_hashname)
                    while self.Lock:
                        sleep(0.1)
                    self.nodes_info.pop(bbb_hashname)
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
        current_list = self.tabWidget.currentIndex()
        if current_list == BASIC_TAB:
            bbb = self.basicList.selectedItems()[0].text()
        elif current_list == ADVANCED_TAB:
            bbb = self.advancedList.selectedItems()[0].text()
        elif current_list == SERVICE_TAB:
            bbb = self.serviceList.selectedItems()[0].text()
        else:
            index = self.logsTable.selectionModel().selectedRows()[0]
            bbb = index.sibling(index.row(), 1).data()
        bbb_ip, bbb_hostname = bbb.split(" - " if current_list != LOGS_TAB else ":")
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
        current_list = self.tabWidget.currentIndex()
        if current_list == BASIC_TAB:
            bbb = self.basicList.selectedItems()[0].text()
        elif current_list == ADVANCED_TAB:
            bbb = self.advancedList.selectedItems()[0].text()
        elif current_list == SERVICE_TAB:
            bbb = self.serviceList.selectedItems()[0].text()
        else:
            index = self.logsTable.selectionModel().selectedRows()[0]
            bbb = index.sibling(index.row(), 1).data()
        bbb_ip, bbb_hostname = bbb.split(" - " if current_list != LOGS_TAB else ":")
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
        current_list = self.tabWidget.currentIndex()
        if current_list == BASIC_TAB:
            bbb = self.basicList.selectedItems()[0].text()
        elif current_list == ADVANCED_TAB:
            bbb = self.advancedList.selectedItems()[0].text()
        elif current_list == SERVICE_TAB:
            bbb = self.serviceList.selectedItems()[0].text()
        else:
            index = self.logsTable.selectionModel().selectedRows()[0]
            bbb = index.sibling(index.row(), 1).data()
        bbb_ip, bbb_hostname = bbb.split(" - " if current_list != LOGS_TAB else ":")
        hashname = "BBB:{}:{}".format(bbb_ip, bbb_hostname)
        info = self.nodes_info[hashname]
        if info[b"state_string"].decode() == "Connected":
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
            "Are you sure applying these changes?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirmation == QtWidgets.QMessageBox.Yes:
            selected_operation = self.operationcomboBox.currentText()
            if selected_operation == "Restart":
                operation = self.server.restart_service
            else:
                operation = self.server.stop_service
            selected_bbbs = self.serviceList.selectedItems()
            for bbb in selected_bbbs:
                bbb_ip, bbb_hostname = bbb.text().split(" - ")
                if self.bbbreadBox.isChecked():
                    operation(bbb_ip, "bbbread", bbb_hostname)
                if self.bbbfunctionBox.isChecked():
                    operation(bbb_ip, "bbb-function", bbb_hostname)


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
    # Display model for TableView
    def __init__(self, data, all=False):
        super(TableModel, self).__init__()
        self._data = data
        self._header = (
            ["Timestamp", "BBB", "Occurence"] if all else ["Timestamp", "Occurence"]
        )

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._header[section]

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self._data[index.row()][index.column()]

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
        self.layoutChanged.emit()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if self.rowCount(0) < 1:
            return 0
        return len(self._data[0])


class BBBLogs(QtWidgets.QWidget, Ui_MainWindow_logs):
    # BBB Logs Display
    def __init__(self, server, hashname):
        QtWidgets.QWidget.__init__(self)
        Ui_MainWindow_logs.__init__(self)
        self.setupUi(self)

        self.logs_thread = UpdateLogsThread(server, hashname)
        self.logs_thread.finished.connect(self.update_table)

        self.model = TableModel([[]])
        self.logsTable.setModel(self.model)

        self.fromTimeEdit.dateTimeChanged.connect(self.update_filters)
        self.toTimeEdit.dateTimeChanged.connect(self.update_filters)

        self.filterEdit.textChanged.connect(self.update_filters)

        self.autoUpdate_timer = QtCore.QTimer(self)
        self.autoUpdate_timer.timeout.connect(self.logs_thread.start)
        self.autoUpdate_timer.setSingleShot(False)
        self.autoUpdate_timer.start(1000)

    def update_table(self, logs, update=True):
        """ Sets table values and converts timestamp, deep copies logs """
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
        """ Updates log table with filters set by user """
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
        for index, r in enumerate(self.data):
            if int(r[0]) < min_date:
                min_index = index
                break

        for index, r in enumerate(self.data[::-1]):
            if int(r[0]) > max_date:
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
