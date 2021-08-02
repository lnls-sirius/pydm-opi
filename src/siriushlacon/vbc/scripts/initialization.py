import logging
import time

from siriushlacon.vbc.epics import ACP, BBB, ProcessOn, ProcessRecovery, Turbovac

logger = logging.getLogger(__name__)


class Initialization:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        self._tick = 0.05

        # Create TURBOVAC PVs
        self.turbovac = Turbovac(prefix=prefix)

        # Create beaglebone PVs
        self.bbb = BBB(prefix=prefix)

        # Create ACP PVs
        self.acp = ACP(prefix=prefix)

        # Create process recovery status PVs
        self.process_recovery = ProcessRecovery(prefix=prefix)

        # Create process ON status PVs
        self.process_on = ProcessOn(prefix=prefix)

    def run(self):
        """if pressure is between 0.05 and 1*10**-8, trigger "process_recovery" script"""
        if (self.bbb.pressure_pv.value < 0.05) & (
            self.bbb.pressure_pv.value > 10 ** -8
        ):
            self._stage_1()
            self._stage_2()
            self._stage_3()
            self._stage_4()
            self._stage_5()

    def _stage_1(self):
        logger.info("stage1")
        self.process_recovery.status1_pv.value = 1

        # turn ACP15 pump ON and wait 30 s
        self.acp.on_off_pv.value = 1

        # set ACP15 speed to maximum (6000 rpm)
        self.acp.speed_rpm.value = 6000

        # wait until pump receives command to turn on
        while self.acp.on_off_pv.value == 0:
            time.sleep(self._tick)

        time.sleep(30)

    def _stage_2(self):
        logger.info("stage2")
        # open pre-vacuum valve
        self.bbb.pre_vacuum_valve_sw_pv.value = 1

        # wait gate valve receives command to open
        while self.bbb.pre_vacuum_valve_sw_pv.value == 0:
            time.sleep(self._tick)

        # update status
        self.process_recovery.status2_pv.value = 1

    def _stage_3(self):
        logger.info("stage3")
        # turn TURBOVAC pump ON
        self.turbovac.pzd1_sp_tevl_pv.value = 1
        self.turbovac.pzd1_sp_zrvl_pv.value = 1

        # wait until pump receives command to turn on
        while (self.turbovac.pzd1_sp_zrvl_pv.value == 0) & (
            self.turbovac.pzd1_sp_tevl_pv.value == 0
        ):
            time.sleep(self._tick)

        self.process_recovery.status3_pv.value = 1

    def _stage_4(self):
        logger.info("stage4")
        # wait TURBOVAC pump reaches 1200 Hz
        self.turbovac.pzd2_sp_pv.value = 1200
        self.turbovac.pzd1_sp_sxvl_pv.value = 1

        while self.turbovac.pzd2_rb_pv.value < 1200:
            time.sleep(self._tick)

        self.turbovac.pzd1_sp_sxvl_pv.value = 0

        self.process_recovery.status4_pv.value = 1

    def _stage_5(self):
        logger.info("stage5")
        # open gate valve (VAT)
        self.bbb.gate_valve_sw_pv.value = 1

        # read gate valve (VAT) status to check if it is really open
        loop = True
        while loop:
            Lo = self.bbb.valve_open_pv.value
            Lg = self.bbb.valve_closed_pv.value
            if Lo & (not Lg):
                loop = False
            time.sleep(self._tick)

        self.process_recovery.status5_pv.value = 1
        self.process_on.activate_all_status()


def initialization(prefix: str):
    """
    this script runs after every boot of BeagleBone Black. It checks whether the
    pressure is lower or higher than 0.05 Torr. In case it's lower than 0.05, then
    run the "process_recovery.py" script.
    """
    init = Initialization(prefix=prefix)
    init.run()
