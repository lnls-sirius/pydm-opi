import logging
import re
import typing

import conscommon.data_model
from pydm.widgets import channel
from qtpy.QtCore import QObject, Signal

logger = logging.getLogger()


class TableDataRow:
    def __init__(
        self,
        device: conscommon.data_model.Device,
        channel: conscommon.data_model.Channel,
        render: bool,
    ) -> None:
        self.device: conscommon.data_model.Device = device
        self.channel: conscommon.data_model.Channel = channel
        self.render: bool = render


class TableDataController(QObject):

    update_content = Signal()

    _table_batch = 24

    def __init__(
        self,
        table,
        devices: typing.List[conscommon.data_model.Device] = None,
        table_batch=24,
        horizontal_header_labels=None,
        **kwargs
    ):
        super().__init__()
        self.devices: typing.List[conscommon.data_model.Device] = (
            devices if devices else []
        )
        self._filter_pattern: typing.Optional[str] = None
        self._table_batch = table_batch

        self.horizontalHeaderLabels = horizontal_header_labels
        self.table = table
        self.table_data: typing.List[TableDataRow] = []

        self.MaxValue = 50
        self.MinValue = 1

        self.batch_offset: int = 0
        self.total_rows: int = 0

        self.init_table()
        self.update_content.connect(self.update_table_content)
        self.update_content.connect(self.resize)

        self.load_table_data()

    def resize(self):
        if self.table:
            self.table.resizeColumnsToContents()

    def init_table(self):
        self.table.setRowCount(self._table_batch)
        self.table.setColumnCount(len(self.horizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.horizontalHeaderLabels)

        # TODO: Impplement ...
        raise NotImplementedError("Subclass must implement abstract method")

    def filter(self, pattern):
        # TODO: Impplement ...
        raise NotImplementedError("Subclass must implement abstract method")

    def load_table_data(self):
        # TODO: Impplement ...
        raise NotImplementedError("Subclass must implement abstract method")

    def update_table_content(self):
        # TODO: Impplement ...
        raise NotImplementedError("Subclass must implement abstract method")

    def disconnect_widget(self, row, col):
        widget = self.table.cellWidget(row, col)
        widget.channel = None

    def connect_widget(
        self, row, col, channel_name=None, macros=None, connect_color=None
    ):
        widget = self.table.cellWidget(row, col)
        if channel_name:
            widget.channel = channel_name
        if macros:
            widget.macros = macros
        if connect_color:
            cell_color = channel.PyDMChannel(
                address="ca://" + channel_name, value_slot=lambda: self.setColor(row)
            )
            cell_color.connect()

    def setColor(
        self, row, col=3
    ):  # Function to define cell color according to the value
        try:
            vmax = self.MaxValue
            vmin = self.MinValue
            range = vmax - vmin
            cell = self.table.cellWidget(row, col)

            if cell.text() != "":
                ActualValue = float(re.match(r"(\d+)\.(\d+)", cell.text()).group())

                if ActualValue < vmin:
                    ActualValue = vmin
                if (ActualValue - vmin) / range <= 0.5:
                    R = int((510 / range) * (ActualValue - vmin))
                    G = 255

                elif ActualValue < 200:
                    if ActualValue > vmax:
                        ActualValue = vmax
                    R = 255
                    G = int(-(510 / range) * (ActualValue - vmax))

                else:
                    return ()
                cell.setStyleSheet("background-color: rgb{}".format((R, G, 00)))
        except Exception:
            print("Problema com setColor")
            logger.exception('Problema com "setColor"')

    def changeBatch(self, increase):
        if increase:
            if self.batch_offset < len(self.table_data):
                self.batch_offset += self._table_batch
                self.update_content.emit()
        else:
            if self.batch_offset != 0:
                self.batch_offset -= self._table_batch
                if self.batch_offset < 0:
                    self.batch_offset = 0
                self.update_content.emit()
