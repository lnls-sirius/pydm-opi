import logging
import time

from siriushlacon.vbc.epics import ACP, BBB, ProcessRecovery, Turbovac

logger = logging.getLogger(__name__)


class ProcessRecoveryAction:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix
        self._tick = 0.05

        self.process_recovery = ProcessRecovery(prefix=self.prefix)
        self.acp = ACP(prefix=self.prefix)
        self.bbb = BBB(prefix=self.prefix)
        self.turbovac = Turbovac(prefix=self.prefix)

    def run(self):
        self._clear_status()
        self._stage_1()
        self._stage_2()
        self._stage_3()
        self._stage_4()
        self._stage_5()

    def _clear_status(self):
        """clear all status PVs"""
        logger.info("clear_status")
        self.process_recovery.set_all_clear()

    def _stage_1(self):
        """Stage 1:"""
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
        """Stage 2:"""
        logger.info("stage2")
        # open pre-vacuum valve
        self.bbb.pre_vacuum_valve_sw_pv.value = 1

        # update UI checkbox status
        # epics.caput(PRE_VACUUM_VALVE_UI, 1)

        # wait pre-vacuum valve receives value to open
        while self.bbb.pre_vacuum_valve_sw_pv.value == 0:
            time.sleep(self._tick)

        self.process_recovery.status2_pv.value = 1

    def _stage_3(self):
        """Stage 3:"""
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
        """Stage 4:"""
        logger.info("stage4")
        # wait TURBOVAC pump reaches 1200 Hz
        self.turbovac.pzd2_sp_pv.value = 1200
        self.turbovac.pzd1_sp_sxvl_pv.value = 1

        while self.turbovac.pzd2_rb_pv_pv.value < 1200:
            time.sleep(self._tick)

        self.turbovac.pzd1_sp_sxvl_pv.value = 0
        self.process_recovery.status4_pv.value = 1

    def _stage_5(self):
        """Stage 5:"""
        logger.info("stage5")
        # open gate valve (VAT)
        self.bbb.gate_valve_sw_pv.value = 1

        # update UI checkbox status
        # epics.caput(GATE_VALVE_UI, 1)

        # ---------------------------------------
        # read gate valve (VAT) status to check if it is really open
        loop = True
        while loop:
            Lo = self.bbb.valve_open_pv.value
            Lg = self.bbb.valve_closed_pv.value
            if Lo & (not Lg):
                loop = False
            time.sleep(self._tick)

        self.process_recovery.status5_pv.value = 1

        # complement value of PV to launch "Process Finished" window
        self.process_recovery.toggle()


def process_recovery(prefix: str):
    """
    this script do all the procedures to recover from a pressurized system (after a
    power failure, for example) if the pressure is in the range (5*10^-2 ~ 1*10^-8).
    It is divided in 5 stages, described as follow:
        -stage 1: turn ACP15 on and wait 30 s
        -stage 2: open pre-vacuum valve
        -stage 3: turn TURBOVAC on
        -stage 4: wait TURBOVAC frequency reaches 1200 Hz
        -stage 5: open gate valve
    """
    action = ProcessRecoveryAction(prefix=prefix)
    action.run()
