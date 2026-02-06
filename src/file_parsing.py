from data_objects import DataObject, DataObjectType, BandDataObject, DosDataObject
from enums import EnergyUnit, SpinOrientation
from utils import *
import regex_pattern

import re
from typing import Protocol


class FileParser(Protocol):
    def feed(self, line: str) -> None: ...
    def build(self) -> list[DataObject]: ...


class BandFileParser:
    def __init__(self, energy_unit: EnergyUnit, data_type: DataObjectType) -> None:
        self.energy_unit = energy_unit
        self.alpha = BandDataObject(data_type)
        self.alpha.spin = SpinOrientation.Alpha
        self.beta = BandDataObject(data_type)
        self.beta.spin = SpinOrientation.Beta
        self.alpha.energy_unit = self.beta.energy_unit = energy_unit

        self.current_spin = SpinOrientation.Alpha

        self.alpha_buffer = []
        self.beta_buffer = []
        self.line_buffer = []

        self.alpha_k_indexes = []
        self.beta_k_indexes = []

    def feed(self, line: str) -> None:
        if line.startswith("#"):
            self._parse_comment(line)
        elif line.startswith("@"):
            return
        else:
            self._parse_data(line)
    
    def _parse_comment(self, line: str) -> None:
        if "NKPT" in line:
            matches = re.findall(regex_pattern.NKPT, line)
            self.alpha.y_count = self.beta.y_count = int(matches[0][1])
            return
        
        if "EFERMI" in line:
            value = float(re.findall(regex_pattern.EFERMI, line)[0])

            if self.energy_unit == EnergyUnit.ElectronVolt:
                value = round(value * 27.21138, 8)

            if self.current_spin == SpinOrientation.Alpha:
                self.alpha.fermi_energy = value
                self.current_spin = SpinOrientation.Beta
            else:
                self.beta.fermi_energy = value
            return
        
        point = re.findall(regex_pattern.KPT_INDEX, line)
        if point:
            idx = int(point[0][0])
            self.alpha_k_indexes.append(idx)
            self.beta_k_indexes.append(idx)

    def _parse_data(self, line: str) -> None:
        values = list(map(float, re.findall(regex_pattern.DATA, line)))
        self.line_buffer += values

        target = self.alpha_buffer if self.current_spin == SpinOrientation.Alpha else self.beta_buffer
        y_count = self.alpha.y_count

        if len(self.line_buffer) == y_count + 1:
            target.append(self.line_buffer)
            self.line_buffer = []
    
    def _finalize_spin(self, data_obj: BandDataObject, data_buffer: list[list[float]], k_indexes: list[int]) -> None:
        buffer_t = transpose(data_buffer)

        data_obj.x_data = buffer_t[0]

        if self.energy_unit == EnergyUnit.ElectronVolt:
            data_obj.y_data = hartree_to_eV(buffer_t[1:])
        else:
            data_obj.y_data = buffer_t[1:]
        
        for i in k_indexes:
            data_obj.kpath_positions.append(data_obj.x_data[i - 1])

    def build(self) -> list[DataObject]:
        self._finalize_spin(self.alpha, self.alpha_buffer, self.alpha_k_indexes)

        if self.beta_buffer:
            self._finalize_spin(self.beta, self.beta_buffer, self.beta_k_indexes)
            return [self.alpha, self.beta]

        return [self.alpha]

class DosFileParser:
    def __init__(self, energy_unit: EnergyUnit, data_type: DataObjectType) -> None:
        self.energy_unit = energy_unit
        self.alpha = DosDataObject(data_type)
        self.alpha.spin = SpinOrientation.Alpha
        self.beta = DosDataObject(data_type)
        self.beta.spin = SpinOrientation.Beta
        self.alpha.energy_unit = self.beta.energy_unit = energy_unit

        self.current_spin = SpinOrientation.Alpha

        self.alpha_buffer = []
        self.beta_buffer = []
        self.line_buffer = []

    def feed(self, line: str) -> None:
        if line.startswith("#"):
            self._parse_comment(line)
        elif line.startswith("@"):
            return
        else:
            self._parse_data(line)
    
    def _parse_comment(self, line: str) -> None:

        if "NEPTS" in line:
            matches = re.findall(regex_pattern.NEPTS, line)
            self.alpha.y_count = self.beta.y_count = int(matches[0][1])
            return

        if "EFERMI" in line:
            value = float(re.findall(regex_pattern.EFERMI, line)[0])

            if self.energy_unit == EnergyUnit.ElectronVolt:
                value = round(value * 27.21138, 8)
            
            if self.current_spin == SpinOrientation.Alpha:
                self.alpha.fermi_energy = value
                self.current_spin = SpinOrientation.Beta
            else:
                self.beta.fermi_energy = value
            return

    def _parse_data(self, line: str) -> None:
        values = list(map(float, re.findall(regex_pattern.DATA, line)))
        self.line_buffer += values

        target = self.alpha_buffer if self.current_spin == SpinOrientation.Alpha else self.beta_buffer
        y_count = self.alpha.y_count

        if len(self.line_buffer) == y_count + 1:
            target.append(self.line_buffer)
            self.line_buffer = []
    
    def _finalize_spin(self, data_obj: DosDataObject, data_buffer: list[list[float]]) -> None:
        buffer_t = transpose(data_buffer)

        data_obj.x_data = buffer_t[0]

        if self.energy_unit == EnergyUnit.ElectronVolt:
            data_obj.x_data = vector_hartree_to_eV(buffer_t[0])
            data_obj.y_data = dos_hartree_to_eV(buffer_t[1:])
        else:
            data_obj.x_data = buffer_t[0]
            data_obj.y_data = buffer_t[1:]

    def build(self) -> list[DataObject]:
        self._finalize_spin(self.alpha, self.alpha_buffer)

        if self.beta_buffer:
            self._finalize_spin(self.beta, self.beta_buffer)
            return [self.alpha, self.beta]

        return [self.alpha]