#!/usr/bin/env python3
import epics
import logging
import math
import asyncio
import sys
import typing
import time
from typing import List

from datetime import timedelta, datetime
from conscommon.data import TIMEFMT
from conscommon.data_model import Device
from siriushlacon.agilent4uhv.tree import DeviceTreeSelection

from qtpy.QtCore import QObject, Signal, QRunnable

logger = logging.getLogger()

EPICS_TOUT = 1
CMD_TOUT = 1.
TIMER_BETWEEN_DEVICES = 0.5

FIXED, STEP, STEP_TO_FIXED = "fixed", "step", "step_to_fixed"


class AgilentAsync(QObject):
    timerStatus = Signal(dict)
    started = Signal()
    finished = Signal()

    def __init__(self, *args, **kwargs):
        super(AgilentAsync, self).__init__(*args, **kwargs)

    async def toFixed(
        self, device: Device, voltage: int, channels_selected: List[bool]
    ):
        self.timerStatus.emit({"device": device.prefix, "status": "to Fixed"})

        pv = device.prefix + ":Step-SP"
        actual_value = epics.caget(device.prefix + ":Step-RB", timeout=EPICS_TOUT)
        if actual_value == None:
            logger.fatal(
                "Failed to get {} value, aborting operation.".format(
                    device.prefix + ":Step-RB"
                )
            )
            self.timerStatus.emit(
                {"device": device.prefix, "status": "failed to get readback"}
            )
            return

        val = actual_value
        for ch, selected, shift in zip(
            device.channels, channels_selected, range(len(channels_selected))
        ):
            if selected:
                val &= ~(1 << shift)

        logger.info(
            "Channel {}  {:04b} -> {:04b} {}".format(
                pv, actual_value, val, channels_selected
            )
        )

        self.timerStatus.emit(
            {
                "device": device.prefix,
                "status": 'to Fixed "{:04b}"->"{:04b}"'.format(actual_value, val),
            }
        )

        if epics.caput(pv, val, timeout=EPICS_TOUT) == 1:
            await asyncio.sleep(CMD_TOUT)

            for ch, selected in zip(device.channels, channels_selected):
                if not selected:
                    continue
                pv, val = ch.prefix + ":VoltageTarget-SP", voltage

                self.timerStatus.emit(
                    {
                        "device": device.prefix,
                        "status": "{} Voltage -> {}V".format(pv, val),
                    }
                )

                logger.info("set {} {}".format(pv, val))
                epics.caput(pv, val, timeout=EPICS_TOUT)

                # @fixme: Two devices at the same serial network should have an actual delay!
                time.sleep(TIMER_BETWEEN_DEVICES)
                await asyncio.sleep(CMD_TOUT)

            self.timerStatus.emit({"device": device.prefix, "status": "Done"})
        else:
            self.timerStatus.emit({"device": device.prefix, "status": "Failed"})

    async def toStep(self, device: Device, channels_selected: List[bool]):
        self.timerStatus.emit({"device": device.prefix, "status": "to Step"})

        pv = device.prefix + ":Step-SP"
        actual_value = epics.caget(device.prefix + ":Step-RB", timeout=EPICS_TOUT)
        if actual_value == None:
            logger.fatal(
                "Failed to get {} value, aborting operation.".format(
                    device.prefix + ":Step-RB"
                )
            )
            self.timerStatus.emit(
                {"device": device.prefix, "status": "failed to get readback"}
            )
            return

        val = actual_value
        n = 0
        for ch, selected in zip(device.channels, channels_selected):
            if selected:
                val |= 1 << n
            n += 1

        self.timerStatus.emit(
            {
                "device": device.prefix,
                "status": "to Step {:04b} -> {:04b}".format(actual_value, val),
            }
        )
        logger.info("Channel {}  {:04b} -> {:04b}".format(pv, actual_value, val))
        if epics.caput(pv, val, timeout=EPICS_TOUT) == 1:
            self.timerStatus.emit({"device": device.prefix, "status": "Done"})
        else:
            self.timerStatus.emit({"device": device.prefix, "status": "Failed"})
        await asyncio.sleep(CMD_TOUT)

    async def doWait(self, device, _delay):
        t_ini = datetime.now()
        delay = timedelta(seconds=_delay)

        tick = math.ceil(_delay / 100)
        t_now = datetime.now()
        t_elapsed = t_now - t_ini
        while t_elapsed < delay:
            remaining = delay - t_elapsed
            logger.info('Time remaining {} for device "{}".'.format(remaining, device))
            self.timerStatus.emit({"device": device.prefix, "status": remaining})
            await asyncio.sleep(tick)

            t_now = datetime.now()
            t_elapsed = t_now - t_ini

        logger.info(
            'Running final function "{}" at {} for device "{}".'.format(
                self.toFixed.__name__, datetime.now().strftime(TIMEFMT), device
            )
        )

    async def toStepToFix(
        self,
        device: Device,
        _delay: float,
        channels_selected,
    ):
        """ Run a function then another ..."""
        logger.info(
            'Running initial function "{}" for device "{}". Next method in {} seconds.'.format(
                self.toStep.__name__, device, _delay
            )
        )
        await self.toFixed(device, 7000, channels_selected=channels_selected)

        await self.doWait(device=device, _delay=_delay)

        await self.toFixed(device, 5000, channels_selected=channels_selected)

        await self.doWait(device=device, _delay=_delay)

        await self.toFixed(device, 3000, channels_selected=channels_selected)

    async def handle(
        self,
        mode,
        step_to_fixed_delay: float,
        voltage: int,
        devices_selection: List[DeviceTreeSelection],
    ):
        if sys.version_info >= (3, 7):
            from asyncio import create_task
        else:
            loop = asyncio.get_event_loop()
            create_task = loop.create_task

        tasks = []
        for sel in devices_selection:
            if mode == FIXED:
                tasks.append(
                    create_task(
                        self.toFixed(
                            sel.device,
                            voltage=voltage,
                            channels_selected=sel.channels_selected,
                        )
                    )
                )

            elif mode == STEP:
                tasks.append(
                    create_task(
                        self.toStep(sel.device, channels_selected=sel.channels_selected)
                    )
                )

            elif mode == STEP_TO_FIXED:
                tasks.append(
                    create_task(
                        self.toStepToFix(
                            _delay=step_to_fixed_delay,
                            device=sel.device,
                            channels_selected=sel.channels_selected,
                        )
                    )
                )
            time.sleep(TIMER_BETWEEN_DEVICES)

        await asyncio.gather(*tasks)

    def asyncStart(
        self, mode, step_to_fixed_delay, voltage, devices_selection,
    ):
        if sys.version_info >= (3, 7):
            from asyncio import run as asyncio_run
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio_run = loop.run_until_complete

        asyncio_run(
            self.handle(
                mode=mode,
                step_to_fixed_delay=step_to_fixed_delay,
                voltage=voltage,
                devices_selection=devices_selection,
            )
        )

        if sys.version_info < (3, 7):
            loop.close()


class AgilentAsyncRunnable(QRunnable):
    def __init__(
        self,
        agilentAsync: AgilentAsync,
        devices_selection: List[DeviceTreeSelection],
        mode,
        step_to_fixed_delay: float,
        voltage: int,
    ):
        super(AgilentAsyncRunnable, self).__init__()
        self.agilentAsync = agilentAsync
        self.mode = mode
        self.step_to_fixed_delay = step_to_fixed_delay
        self.voltage = voltage
        self.devices_selection = devices_selection

    def run(self):
        self.agilentAsync.started.emit()
        try:
            self.agilentAsync.asyncStart(
                mode=self.mode,
                step_to_fixed_delay=self.step_to_fixed_delay,
                voltage=self.voltage,
                devices_selection=self.devices_selection,
            )
        except Exception:
            logger.exception("Unexpected Error")
        finally:
            self.agilentAsync.finished.emit()
