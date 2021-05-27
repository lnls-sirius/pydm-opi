import logging
import time

from siriushlacon.vbc.epics import ACP, BBB, ProcessOff, ProcessOn, System, Turbovac

logger = logging.getLogger(__name__)


class ProcessOnAction:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix
        self._tick = 0.05

        self.process_on = ProcessOn(prefix=self.prefix)
        self.process_off = ProcessOff(prefix=self.prefix)
        self.turbovc = Turbovac(prefix=self.prefix)
        self.bbb = BBB(prefix=self.prefix)
        self.acp = ACP(prefix=self.prefix)
        self.system = System(prefix=self.prefix)

    def run(self):
        self._clear_status()
        self._stage_1()
        self._stage_2()
        self._stage_3()
        self._stage_4()
        self._stage_5()

    def _clear_status(self):
        logger.info("Clear status")
        # clear all status PVs
        self.process_on.clear_all_status()
        self.process_off.clear_all_fv_status()

    def _stage_1(self):
        """wait TURBOVAC pump stops completely"""
        logger.info("Stage 1")
        self.process_on.status1_pv.value = 1

        while self.turbovc.pzd2_rb_pv.value != 0:
            time.sleep(self._tick)

    def _stage_2(self):
        """Stage 2:"""
        logger.info("Stage 2")
        # open gate valve (VAT) and the pre-vacuum valve
        self.bbb.gate_valve_sw_pv.value = 1
        self.bbb.pre_vacuum_valve_sw_pv.value = 1

        # update UI checkbox status
        # epics.caput(GATE_VALVE_UI, 1)
        # epics.caput(PRE_VACUUM_VALVE_UI, 1)

        # ---------------------------------------
        # wait gate valve receives command to open
        while self.bbb.pre_vacuum_valve_sw_pv.value == 0:
            time.sleep(self._tick)

        # read gate valve (VAT) status to check if it is really open
        loop = True
        while loop:
            Lo = self.bbb.valve_open_pv.value
            Lg = self.bbb.valve_closed_pv.value

            if Lo & (not (Lg)):
                loop = False
            time.sleep(self._tick)

        self.process_on.status2_pv.value = 1

    def _stage_3(self):
        """Stage 3:"""
        logger.info("Stage 3")
        # turn ACP15 pump ON
        self.acp.on_off_pv.value = 1
        # wait until pump receives command to turn on
        while self.acp.on_off_pv.value == 0:
            time.sleep(self._tick)

        self.process_on.status3_pv.value = 1

    def check_pressure_limits(self) -> bool:
        """Is pressure under 5*(10^-2) Torr"""
        return self.bbb.pressure_pv.value > (
            self.system.on_pressure_base_pv.value
            * 10 ** self.system.on_pressure_exp_pv.value
        )

    def _stage_4(self):
        """Stage 4: read the pressure and proceed when its value is under 5*(10^-2) Torr"""
        logger.info("Stage 4")
        while self.check_pressure_limits():
            time.sleep(self._tick)

        self.process_on.status4_pv.value = 1

    def _stage_5(self):
        """Stage 5:"""
        logger.info("Stage 5")
        # turn TURBOVAC pump ON
        self.turbovc.pzd1_sp_tevl_pv.value = 1
        self.turbovc.pzd1_sp_zrvl_pv.value = 1

        # wait until pump receives command to turn on
        while (self.turbovc.pzd1_sp_tevl_pv.value == 0) & (
            self.turbovc.pzd1_sp_zrvl_pv.value == 0
        ):
            time.sleep(self._tick)

        self.process_on.status5_pv.value = 1

        # complement value of PV to launch "Process Finished" window
        self.process_on.toggle()


def process_on(prefix: str):
    """
    this script do all the procedures to decrease the pressure of the system
    it is divided in 5 stages, described as follow:
        -stage 1: open gate and pre-vacuum valves (and wait gate valve really closes)
        -stage 2: wait until gate valve actually closes
        -stage 3: turn ACP15 on
        -stage 4: wait pressure decrease to less than 0.05 Torr
        -stage 5: turn TURBOVAC on
    """
    action = ProcessOnAction(prefix=prefix)
    action.run()
