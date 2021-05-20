import epics


def check_pressure_script(prefix: str, first_time: bool):
    """
    this script runs after the user hits the "ON" button under the "system_tab.ui"
    window. It checks whether the pressure is lower or higher than 0.05 Torr.
    - if it's value is higher than 0.05, then the "process_on" script is executed
    - if it's value is lower, then the "system_pressurized" window will pop-up
    """
    pressure_pv = epics.PV(pvname=f"{prefix}:BBB:Torr")
    torr_base_pv = epics.PV(pvname=f"{prefix}:BBB:TorrBase")
    torr_exp_pv = epics.PV(pvname=f"{prefix}:BBB:TorrExp")

    torr_base_msg_pv = epics.PV(pvname=f"{prefix}:BBB:TorrBaseMsg")
    torr_exp_msg_pv = epics.PV(pvname=f"{prefix}:BBB:TorrExpMsg")

    process_trigger_on_pv = epics.PV(pvname=f"{prefix}:Process:TriggerOn")
    process_trigger_pressurized_pv = epics.PV(
        pvname=f"{prefix}:Process:TriggerPressurized"
    )

    torr_base_msg_pv.value = torr_base_pv.value
    torr_exp_msg_pv.value = torr_exp_pv.value

    # update value showed in "system_pressurized.ui" window
    # if pressure value is bigger than 0.05 Torr, trigger "process_on" script
    if pressure_pv.value > 0.05:
        if not first_time:
            process_trigger_on_pv.value = 1
            process_trigger_on_pv.value = 0

    # if pressure is between 0.05 and 1*10**-8, trigger "process_recovery" script
    elif (pressure_pv.value < 0.05) & (pressure_pv.value > 10 ** -8):
        process_trigger_pressurized_pv.value = 1
        process_trigger_pressurized_pv.value = 0
