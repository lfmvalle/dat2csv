from typing import Protocol
from abc import ABC

from enums import DataObjectType, SpinOrientation, EnergyUnit
from utils import Vector, Matrix


class DataObject(Protocol):
    data_type: DataObjectType
    spin: SpinOrientation
    x_data: Vector
    y_data: Matrix
    y_count: int
    fermi_energy: float
    energy_unit: EnergyUnit


class AbstractDataObject(ABC):
    def __init__(self, data_type: DataObjectType) -> None:
        self.data_type = data_type
        self.spin: SpinOrientation
        self.x_data: Vector
        self.y_count: int
        self.y_data: Matrix
        self.fermi_energy: float
        self.energy_unit: EnergyUnit


class BandDataObject(AbstractDataObject):
    def __init__(self, data_type: DataObjectType) -> None:
        super().__init__(data_type)
        self.kpath_positions: Vector = []


class DosDataObject(AbstractDataObject):
    def __init__(self, data_type: DataObjectType) -> None:
        super().__init__(data_type)