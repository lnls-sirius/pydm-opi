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

    def set_all_active(self):
        self.status1_pv.value = 1
        self.status2_pv.value = 1
        self.status3_pv.value = 1
        self.status4_pv.value = 1
        self.status5_pv.value = 1


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

        self.valve_open_pv = create_connected_pv(pvname=f"{self.prefix}:BBB:ValveOpen")
        self.valve_closed_pv = create_connected_pv(
            pvname=f"{self.prefix}:BBB:ValveClosed"
        )


class Turbovac:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        # turn TURBOVAC pump ON
        self.pzd1_sp_tevl_pv = create_connected_pv(
            pvname=f"{self.prefix}:TURBOVAC:PZD1-SP.TEVL"
        )
        self.pzd1_sp_zrvl_pv = create_connected_pv(
            pvname=f"{self.prefix}:TURBOVAC:PZD1-SP.ZRVL"
        )

        # wait TURBOVAC pump reaches 1200 Hz
        self.pzd1_sp_sxvl_pv = create_connected_pv(
            pvname=f"{self.prefix}:TURBOVAC:PZD1-SP.SXVL"
        )
        self.pzd2_rb_pv = create_connected_pv(pvname=f"{self.prefix}:TURBOVAC:PZD2-RB")
        self.pzd2_sp_pv = create_connected_pv(pvname=f"{self.prefix}:TURBOVAC:PZD2-SP")


class ACP:
    def __init__(self, prefix: str):
        if not prefix:
            raise ValueError(f"parameter prefix cannot be empty {prefix}")
        self.prefix = prefix

        self.on_off_pv = create_connected_pv(pvname=f"{self.prefix}:ACP:OnOff")
        self.speed_rpm = create_connected_pv(pvname=f"{self.prefix}:ACP:SpeedRPM")
