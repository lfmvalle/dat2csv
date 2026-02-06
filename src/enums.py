from enum import Enum


class DataObjectType(Enum):
    Band = "band"
    DOS = "dos"
    COHP = "cohp"
    COOP = "coop"


class SpinOrientation(Enum):
    Alpha = 1
    Beta = -1


class EnergyUnit(Enum):
    Hartree = 0
    ElectronVolt = 1