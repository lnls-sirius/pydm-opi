import datetime
import logging
import asyncio
import requests

from pydm import Display
from qtpy.QtCore import QDateTime
from qtpy.QtWidgets import QTreeWidgetItem

from siriushlacon.regatron.consts import (
    ALARM_UI,
    STD_READINGS,
    EXT_READINGS,
)
from siriushlacon.utils.alarm import Alarm, Severity
from siriushlacon.utils.archiver import get_data_from_archiver
from siriushlacon.utils.consts import SP_TZ

logger = logging.getLogger()


class AlarmDisplay(Display):
    """
    Query alarms from the archiver appliance and display in a human readable format
    """

    @staticmethod
    def reading_tree_item(reading):
        """
        Get data from archiver and transform into a node with branches according to the bit value defined by the mapping.

        :param reading: A data item from the archiver request
        representing the bit position starting from zero and the key is a string with it's meaning
        :return: A QTreeWidgetItem
        """
        # Timestamp
        timestamp = str(
            datetime.datetime.fromtimestamp(reading["secs"]).astimezone(SP_TZ)
        )
        severity = Severity.nameOf(reading["severity"])
        alarm_status = Alarm.nameOf(reading["status"])
        value = reading["val"]

        node = QTreeWidgetItem(
            ["{} {} {} {}".format(timestamp, value, severity, alarm_status)]
        )

        for i in range(32):
            if value & 1 << i:
                node_child = QTreeWidgetItem(["{:X}".format(i)])
                node.addChild(node_child)

        return node

    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=ALARM_UI)
        self.macros = macros
        self.btnNow.clicked.connect(self.set_time_now)
        self.btnSearch.clicked.connect(self.search_alarms)

        # Tree Widget
        self.treeStdWarn.setColumnCount(1)
        self.treeStdWarn.setHeaderLabels(["Standard Warning"])

        self.treeStdErr.setColumnCount(1)
        self.treeStdErr.setHeaderLabels(["Standard Error"])

        self.treeExtWarn.setColumnCount(1)
        self.treeExtWarn.setHeaderLabels(["Extended Warning"])

        self.treeExtErr.setColumnCount(1)
        self.treeExtErr.setHeaderLabels(["Extended Error"])

        self.set_time_now()
        self.search_alarms()

    def get_PV(self, signal, std=False, error=False):
        """
        Build a PV name

        :param signal: Signal name, the last component of the PV
        :param std: True for 'Std' else 'Ext'
        :param error: True for 'Err' else 'Warn'
        :return: the PV name
        """
        return "{}:{}-{}{}".format(
            self.macros["P"], self.macros["T"], "Err" if error else "Warn", signal,
        )

    def set_time_now(self):
        """ Set current date and time to the "dfTo" widget """
        self.dtTo.setDateTime(QDateTime.currentDateTime())

    def do_search(self, time_to, time_from, std, error):
        """
        Query and build the alarm tree

        :param time_to: final time
        :param time_from: initial time
        :param std: True for 'Std' else 'Ext', defines if it's a standard or extended alarm
        :param error: True for 'Err' else 'Warn', defines if it's an error or a warning
        """
        loop = asyncio.get_event_loop()
        futures = []
        # For each PV
        for signal in [*(STD_READINGS if std else EXT_READINGS)]:
            pv = self.get_PV(signal, std=std, error=error)
            futures.append(
                loop.run_in_executor(
                    None, get_data_from_archiver, pv, time_from, time_to, False
                )
            )
        return futures

    def update_alarm_tree(self, alarm_tree, response: requests.Response):
        """
        Build the alarm tree
        :param alarm_tree: QTreeWidget to append the alarms
        :param responses: typing.List[requests.Response]
        """

        # For each PV
        # for response in responses:
        if response.status_code != 200:
            logger.warning(
                "Invalid status code for request. Response {}".format(response)
            )
            logger.debug(response.text)
            return
        try:
            if len(response.json()) < 0:
                logger.info("empty response")
                return

            json_data = response.json()[0]

            pv_node = QTreeWidgetItem(["{}".format(json_data["meta"]["name"])])
            alarm_tree.addTopLevelItem(pv_node)
            for data in response.json()[0]["data"]:
                if data["val"] == 0:
                    # Will not display alarms, only actual value changes
                    continue

                pv_node_child = self.reading_tree_item(data)
                pv_node.addChild(pv_node_child)
        except:
            logger.exception("Failed to add node")

    async def search(self):
        time_to = self.dtTo.dateTime().toPyDateTime().astimezone(SP_TZ)
        time_from = self.dtFrom.dateTime().toPyDateTime().astimezone(SP_TZ)
        async_responses = []

        async_responses.append(
            (
                self.treeStdWarn,
                self.do_search(
                    time_to=time_to, time_from=time_from, std=True, error=False,
                ),
            )
        )
        async_responses.append(
            (
                self.treeStdErr,
                self.do_search(
                    time_to=time_to, time_from=time_from, std=True, error=True,
                ),
            )
        )
        async_responses.append(
            (
                self.treeExtWarn,
                self.do_search(
                    time_to=time_to, time_from=time_from, std=False, error=False,
                ),
            )
        )
        async_responses.append(
            (
                self.treeExtErr,
                self.do_search(
                    time_to=time_to, time_from=time_from, std=False, error=True,
                ),
            )
        )
        for widget, futures in async_responses:
            widget.clear()
            for response in await asyncio.gather(*futures):
                self.update_alarm_tree(widget, response)

    def search_alarms(self):
        """ Update all tree widgets """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.search())
