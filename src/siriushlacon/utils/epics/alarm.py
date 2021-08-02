class Severity:
    NO_ALARM = 0
    MINOR_ALARM = 1
    MAJOR_ALARM = 2
    INVALID_ALARM = 3

    @staticmethod
    def nameOf(index):
        return SeverityStrings[index]


class Alarm:
    NO_ALARM = 0
    READ_ALARM = 1
    WRITE_ALARM = 2
    HIHI_ALARM = 3
    HIGH_ALARM = 4
    LOLO_ALARM = 5
    LOW_ALARM = 6
    STATE_ALARM = 7
    COS_ALARM = 8
    COMM_ALARM = 9
    TIMEOUT_ALARM = 10
    HW_LIMIT_ALARM = 11
    CALC_ALARM = 12
    SCAN_ALARM = 13
    LINK_ALARM = 14
    SOFT_ALARM = 15
    BAD_SUB_ALARM = 16
    UDF_ALARM = 17
    DISABLE_ALARM = 18
    SIMM_ALARM = 19
    READ_ACCESS_ALARM = 20
    WRITE_ACCESS_ALARM = 21

    @staticmethod
    def nameOf(index):
        return AlarmStrings[index]


SeverityStrings = ["NO_ALARM", "MINOR", "MAJOR", "INVALID"]

AlarmStrings = [
    "NO_ALARM",
    "READ",
    "WRITE",
    "HIHI",
    "HIGH",
    "LOLO",
    "LOW",
    "STATE",
    "COS",
    "COMM",
    "TIMEOUT",
    "HWLIMIT",
    "CALC",
    "SCAN",
    "LINK",
    "SOFT",
    "BAD_SUB",
    "UDF",
    "DISABLE",
    "SIMM",
    "READ_ACCESS",
    "WRITE_ACCESS",
]
