from siriushlacon.utils.epics import create_connected_pv


class ProcessOn:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        self.status1_pv = create_connected_pv(pvname=f"{self.prefix}:ProcessOn:Status1")
        self.status2_pv = create_connected_pv(pvname=f"{self.prefix}:ProcessOn:Status2")
        self.status3_pv = create_connected_pv(pvname=f"{self.prefix}:ProcessOn:Status3")
        self.status4_pv = create_connected_pv(pvname=f"{self.prefix}:ProcessOn:Status4")
        self.status5_pv = create_connected_pv(pvname=f"{self.prefix}:ProcessOn:Status5")

        self.bool = create_connected_pv(pvname=f"{self.prefix}:ProcessOn:Bool")

    def activate_all_status(self):
        self.status1_pv.value = 1
        self.status2_pv.value = 1
        self.status3_pv.value = 1
        self.status4_pv.value = 1
        self.status5_pv.value = 1

    def clear_all_status(self):
        self.status1_pv.value = 0
        self.status2_pv.value = 0
        self.status3_pv.value = 0
        self.status4_pv.value = 0
        self.status5_pv.value = 0

    def toggle(self):
        self.bool.value = 1
        self.bool.value = 0


class ProcessOff:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        self.off_fv_status1_pv = create_connected_pv(
            pvname=f"{prefix}:ProcessOffFV:Status1"
        )
        self.off_fv_status2_pv = create_connected_pv(
            pvname=f"{prefix}:ProcessOffFV:Status2"
        )
        self.off_fv_status3_pv = create_connected_pv(
            pvname=f"{prefix}:ProcessOffFV:Status3"
        )
        self.off_fv_status4_pv = create_connected_pv(
            pvname=f"{prefix}:ProcessOffFV:Status4"
        )
        self.off_fv_status5_pv = create_connected_pv(
            pvname=f"{prefix}:ProcessOffFV:Status5"
        )
        self.off_fv_status6_pv = create_connected_pv(
            pvname=f"{prefix}:ProcessOffFV:Status6"
        )

        self.bool = create_connected_pv(pvname=f"{self.prefix}:ProcessOff:Bool")

    def toggle(self):
        """turn on and off {self.prefix}:Process:Bool PV"""
        self.bool.value = 1
        self.bool.value = 0

    def clear_all_fv_status(self):
        self.off_fv_status1_pv.value = 0
        self.off_fv_status2_pv.value = 0
        self.off_fv_status3_pv.value = 0
        self.off_fv_status4_pv.value = 0
        self.off_fv_status5_pv.value = 0
        self.off_fv_status6_pv.value = 0


class ProcessRecovery:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        # Create process recovery status PVs
        self.status1_pv = create_connected_pv(
            pvname=f"{self.prefix}:ProcessRecovery:Status1"
        )
        self.status2_pv = create_connected_pv(
            pvname=f"{self.prefix}:ProcessRecovery:Status2"
        )
        self.status3_pv = create_connected_pv(
            pvname=f"{self.prefix}:ProcessRecovery:Status3"
        )
        self.status4_pv = create_connected_pv(
            pvname=f"{self.prefix}:ProcessRecovery:Status4"
        )
        self.status5_pv = create_connected_pv(
            pvname=f"{self.prefix}:ProcessRecovery:Status5"
        )

        self.bool = create_connected_pv(pvname=f"{self.prefix}:ProcessRec:Bool")

    def toggle(self):
        self.bool.value = 1
        self.bool.value = 0

    def set_all_clear(self):
        self.status1_pv.value = 0
        self.status2_pv.value = 0
        self.status3_pv.value = 0
        self.status4_pv.value = 0
        self.status5_pv.value = 0


class BBB:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        self.pressure_pv = create_connected_pv(pvname=f"{self.prefix}:BBB:Torr")
        self.pre_vacuum_valve_sw_pv = create_connected_pv(
            pvname=f"{self.prefix}:BBB:Relay1-SW"
        )

        self.gate_valve_sw_pv = create_connected_pv(
            pvname=f"{self.prefix}:BBB:Relay2-SW"
        )
        self.gate_valve_ui_pv = create_connected_pv(
            pvname=f"{self.prefix}:BBB:Relay2-UI"
        )

        self.valve_open_pv = create_connected_pv(pvname=f"{self.prefix}:BBB:ValveOpen")
        self.valve_closed_pv = create_connected_pv(
            pvname=f"{self.prefix}:BBB:ValveClosed"
        )


class Turbovac:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        self.pzd1_sp_tevl_pv = create_connected_pv(
            pvname=f"{self.prefix}:TURBOVAC:PZD1-SP.TEVL"
        )
        self.pzd1_sp_zrvl_pv = create_connected_pv(
            pvname=f"{self.prefix}:TURBOVAC:PZD1-SP.ZRVL"
        )
        self.pzd1_sp_sxvl_pv = create_connected_pv(
            pvname=f"{self.prefix}:TURBOVAC:PZD1-SP.SXVL"
        )

        self.pzd2_rb_pv = create_connected_pv(pvname=f"{self.prefix}:TURBOVAC:PZD2-RB")
        self.pzd2_sp_pv = create_connected_pv(pvname=f"{self.prefix}:TURBOVAC:PZD2-SP")

        self.ak_sp_pv = create_connected_pv(pvname=f"{self.prefix}:TURBOVAC:AK-SP")
        self.ind_sp_pv = create_connected_pv(pvname=f"{self.prefix}:TURBOVAC:IND-SP")
        self.pnu_sp_pv = create_connected_pv(pvname=f"{self.prefix}:TURBOVAC:PNU-SP")
        self.pwe_sp_pv = create_connected_pv(pvname=f"{self.prefix}:TURBOVAC:PWE-SP")

        self.pre_vacuum_valve_sw_pv = create_connected_pv(
            pvname=f"{self.prefix}:BBB:Relay1-SW"
        )

        self.venting_valve_sw_pv = create_connected_pv(
            pvname=f"{self.prefix}:TURBOVAC:VentingValve-SW"
        )
        self.venting_valve_ui_pv = create_connected_pv(
            pvname=f"{self.prefix}:TURBOVAC:VentingValve-UI"
        )


class System:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix
        self.off_frequency_pv = create_connected_pv(
            pvname=f"{self.prefix}:SYSTEM:OffFrequency"
        )
        self.off_pressure_base_pv = create_connected_pv(
            pvname=f"{self.prefix}:SYSTEM:OffPressureBase"
        )
        self.off_pressure_exp_pv = create_connected_pv(
            pvname=f"{self.prefix}:SYSTEM:OffPressureExp"
        )

        self.on_pressure_base_pv = create_connected_pv(
            pvname=f"{self.prefix}:SYSTEM:OnPressureBase"
        )
        self.on_pressure_exp_pv = create_connected_pv(
            pvname=f"{self.prefix}:SYSTEM:OnPressureExp"
        )


class ACP:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        self.on_off_pv = create_connected_pv(pvname=f"{self.prefix}:ACP:OnOff")
        self.speed_rpm = create_connected_pv(pvname=f"{self.prefix}:ACP:SpeedRPM")
