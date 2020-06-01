#!/usr/bin/env python3
import epics
import logging
import math
import asyncio
import sys
from typing import List

from datetime import timedelta, datetime
from conscommon.data import TIMEFMT
from conscommon.data_model import Device

from qtpy.QtCore import QObject, Signal, QRunnable

logger = logging.getLogger()

EPICS_TOUT = 1
CMD_TOUT = 0.500

FIXED, STEP, STEP_TO_FIXED = "fixed", "step", "step_to_fixed"


class AgilentAsync(QObject):
    timerStatus = Signal(dict)
    started = Signal()
    finished = Signal()

    def __init__(self, *args, **kwargs):
        super(AgilentAsync, self).__init__(*args, **kwargs)

    async def toFixed(
        self, device: Device, voltage: int,
    ):
        self.timerStatus.emit({"device": device.prefix, "status": "to Fixed"})

        pv, val = device.prefix + ":Step-SP_Backend", 0
        logger.info("set {} {}".format(pv, val))

        if True:  # epics.caput(pv, val, timeout=EPICS_TOUT) == 1:
            await asyncio.sleep(CMD_TOUT)

            for ch in device.channels:
                pv, val = ch.prefix + ":VoltageTarget-SP", voltage

                logger.info("set {} {}".format(pv, val))
                # epics.caput(pv, val, timeout=EPICS_TOUT)
                await asyncio.sleep(CMD_TOUT)

            self.timerStatus.emit({"device": device.prefix, "status": "Done"})
        else:
            self.timerStatus.emit({"device": device.prefix, "status": "Failed"})

    async def toStep(
        self, device: Device,
    ):
        self.timerStatus.emit({"device": device.prefix, "status": "to Step"})

        pv, val = device.prefix + ":Step-SP_Backend", 15
        logger.info("set {} {}".format(pv, val))
        if True:  # epics.caput(pv, val, timeout=EPICS_TOUT) == 1:
            self.timerStatus.emit({"device": device.prefix, "status": "Done"})
        else:
            self.timerStatus.emit({"device": device.prefix, "status": "Failed"})
        await asyncio.sleep(CMD_TOUT)

    async def toStepToFix(
        self, device: Device, voltage: int, _delay: float,
    ):
        """ Run a function then another ..."""
        delay = timedelta(seconds=_delay)
        t_ini = datetime.now()

        tick = math.ceil(_delay / 100)

        logger.info(
            'Running initial function "{}" at {} for device "{}". Next method in {} seconds.'.format(
                self.toStep.__name__, t_ini.strftime(TIMEFMT), device, _delay
            )
        )
        await self.toStep(device)

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

        await self.toFixed(device, voltage)

    async def handle(
        self, mode, step_to_fixed_delay: float, voltage: int, devices: List[Device]
    ):
        if sys.version_info >= (3, 7):
            from asyncio import create_task
        else:
            loop = asyncio.get_event_loop()
            create_task = loop.create_task

        tasks = []
        for device in devices:
            if mode == FIXED:
                tasks.append(create_task(self.toFixed(device, voltage=voltage,)))

            elif mode == STEP:
                tasks.append(create_task(self.toStep(device)))

            elif mode == STEP_TO_FIXED:
                tasks.append(
                    create_task(
                        self.toStepToFix(
                            _delay=step_to_fixed_delay, device=device, voltage=voltage,
                        )
                    )
                )

        await asyncio.gather(*tasks)

    def asyncStart(
        self, mode, step_to_fixed_delay, voltage, devices,
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
                devices=devices,
            )
        )

        if sys.version_info < (3, 7):
            loop.close()


class AgilentAsyncRunnable(QRunnable):
    def __init__(
        self,
        agilentAsync: AgilentAsync,
        devices: List[Device],
        mode,
        step_to_fixed_delay: float,
        voltage: int,
    ):
        super(AgilentAsyncRunnable, self).__init__()
        self.agilentAsync = agilentAsync
        self.mode = mode
        self.step_to_fixed_delay = step_to_fixed_delay
        self.voltage = voltage
        self.devices = devices

    def run(self):
        self.agilentAsync.started.emit()
        try:
            self.agilentAsync.asyncStart(
                mode=self.mode,
                step_to_fixed_delay=self.step_to_fixed_delay,
                voltage=self.voltage,
                devices=self.devices,
            )
        except Exception:
            logger.exception("Unexpected Error")
        finally:
            self.agilentAsync.finished.emit()
