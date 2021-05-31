import logging
import time

from siriushlacon.vbc.epics import ACP, BBB, ProcessOff, ProcessOn, System, Turbovac

logger = logging.getLogger(__name__)


class ProcessOffAction:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix
        self._tick = 0.05

        self.process_on = ProcessOn(prefix=prefix)
        self.process_off = ProcessOff(prefix=prefix)
        self.bbb = BBB(prefix=prefix)
        self.turbovac = Turbovac(prefix=prefix)
        self.acp = ACP(prefix=prefix)
        self.system = System(prefix=prefix)

    def run(self):
        self._clear_pvs()
        self._stage_1()
        self._stage_2()
        self._stage_3()
        self._stage_4()
        self._stage_5()
        self._stage_6()

    def _clear_pvs(self):
        """clear all status PVs"""
        logger.info("clear_pvs")
        self.process_off.clear_all_fv_status()
        self.process_on.clear_all_status()

    def _stage_1(self):
        logger.info("stage1")
        # close pre-vacuum valve (and keeps gate valve open)
        self.turbovac.pre_vacuum_valve_sw_pv.value = 0

        # wait until valve receives command to open
        while self.turbovac.pre_vacuum_valve_sw_pv.value:
            time.sleep(self._tick)

        self.process_off.off_fv_status1_pv.value = 1

    def _stage_2(self):
        logger.info("stage2")
        # change venting valve to manual control
        self.turbovac.ak_sp_pv.value = 0
        self.turbovac.pnu_sp_pv.value = 134
        self.turbovac.ind_sp_pv.value = 2
        self.turbovac.pwe_sp_pv.value = 18
        self.turbovac.ak_sp_pv.value = 7

        # turn TURBOVAC and ACP15 pumps OFF
        self.turbovac.pzd1_sp_zrvl_pv.value = 0
        self.acp.on_off_pv.value = 0

        # wait until pump receives command to turn off
        while self.acp.on_off_pv.value:
            time.sleep(self._tick)

        self.process_off.off_fv_status2_pv.value = 1

    def _stage_3(self):
        """wait until TURBOVAC frequency decrease to 600 Hz"""
        logger.info("stage3")
        while self.turbovac.pzd2_rb_pv.value > self.system.off_frequency_pv.value:
            time.sleep(self._tick)

        self.process_off.off_fv_status3_pv.value = 1

    def _stage_4(self):
        logger.info("stage4")
        # open X203 valve (TURBOVAC venting valve)
        self.turbovac.venting_valve_sw_pv.value = 1

        # update UI checkbox status
        self.turbovac.venting_valve_ui_pv_rval.value = 1

        # wait until venting valve receives command to close
        while self.turbovac.venting_valve_sw_pv.value == 0:
            time.sleep(self._tick)

        self.process_off.off_fv_status4_pv.value = 1

    def _check_bbb_less_than_off_pressure(self) -> bool:
        bbb_off_pressure = (
            self.system.off_pressure_base_pv.value
            * 10 ** self.system.off_pressure_exp_pv.value
        )
        return self.bbb.pressure_pv.value < bbb_off_pressure

    def _stage_5(self):
        logger.info("stage5")
        while self._check_bbb_less_than_off_pressure():
            time.sleep(self._tick)

        self.process_off.off_fv_status5_pv.value = 1

    def _stage_6(self):
        """Stage 6:"""
        logger.info("stage6")

        # close all the valves (gate valve is already closed)
        self.bbb.gate_valve_sw_pv.value = 0
        self.turbovac.venting_valve_sw_pv.value = 0  # close X203
        self.bbb.gate_valve_ui_pv.value = 0
        self.turbovac.venting_valve_ui_pv_rval.value = 0  # close X203

        # wait until venting valve receives command to close
        while self.bbb.gate_valve_sw_pv.value:
            time.sleep(self._tick)

        self.process_off.off_fv_status6_pv.value = 1

        # complement value of PV to launch "Process Finished" window
        self.process_off.toggle()


def process_off(prefix: str):
    """
    this script do all the procedures turn off the system with full ventilation
    it is divided in 6 stages, described as follow:
        -stage 1: close pre-vacuum valve (keep gate valve open)
        -stage 2: turn ACP15 and TURBOVAC pumps off
        -stage 3: wait TURBOVAC slowdown to 600 Hz
        -stage 4: open X203 (TURBOVAC venting valve)
        -stage 5: wait pressure decrease to 760 Torr
        -stage 6: close X203 and gate valves
    """
    action = ProcessOffAction(prefix=prefix)
    action.run()
