from typing import Generator
from pathlib import Path
import sys

from enums import EnergyUnit
from logger import log_info, log_warn
from exceptions import SysArgvError
import text_style


type Vector = list[float]
type Matrix = list[list[float]]

EV2HA_FACTOR = 27.211386
ROUNDING_FACTOR = 8

def transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]

def ha2eV_value(value: float) -> float:
    return round(value * EV2HA_FACTOR, ROUNDING_FACTOR)

def ha2eV_state(value: float) -> float:
    return round(value / EV2HA_FACTOR, ROUNDING_FACTOR)

def ha2eV_vector(vector: Vector) -> Vector:
    return list(map(lambda value: ha2eV_value(value), vector))

def ha2eV_matrix(matrix: Matrix) -> Matrix:
    return [ha2eV_vector(row) for row in matrix]

def ha2eV_state_matrix(matrix: Matrix) -> Matrix:
    return [list(map(lambda value: ha2eV_state(value), row)) for row in matrix]

def iter_lines(path: Path) -> Generator[str]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

def validate_file(filepath: str) -> bool:
    if not filepath: return False
    if not filepath.lower().endswith(".dat"): return False
    if not any(s in filepath.lower() for s in ["band", "doss", "cohp", "coop"]): return False
    file = Path(filepath)
    if not file.exists(): return False
    if not file.is_file(): return False
    return True

def get_energy_unit() -> EnergyUnit:
    if "-h" in sys.argv:
        log_info(f"Energy data will be kept in {text_style.BOLDITALIC}Hartree{text_style.NONE}.\n         Density of States in {text_style.BOLDITALIC}(states/Hartree)/cell{text_style.NONE}.")
        sys.argv.remove("-h")
        return EnergyUnit.Hartree
    log_info(f"Energy data will be converted to {text_style.BOLDITALIC}eV{text_style.NONE} (default).\n         Density of States now in {text_style.BOLDITALIC}(states/eV)/cell{text_style.NONE}.\n         Use the {text_style.BOLDITALIC}-h{text_style.NONE} argument if you intend to keep Hartree units.")
    return EnergyUnit.ElectronVolt

def validate_arguments() -> None:
    if not len(sys.argv) > 1:
        raise SysArgvError(f"Invalid number of arguments on script call. At least one file must be provided.")
    log_info(f"Validating {text_style.BOLD}{text_style.PURPLE}{len(sys.argv[1:])}{text_style.NONE} argument(s)...")
    initial_count = len(sys.argv[1:])
    all_ok = True
    for argument in sys.argv[1:]:
        if not validate_file(argument):
            all_ok = False
            log_warn(f"Invalid argument: {text_style.BOLDITALIC}{argument}{text_style.NONE}.")
            sys.argv.remove(argument)
    if not all_ok:
        log_info(f"Invalid arguments are automatically ignored by the program.\n         Make sure that the file(s):\n           - contain {text_style.BOLDITALIC}BAND{text_style.NONE}, {text_style.BOLDITALIC}DOSS{text_style.NONE}, {text_style.BOLDITALIC}COOP{text_style.NONE}, or {text_style.BOLDITALIC}COHP{text_style.NONE} in the name;\n           - ends with the {text_style.BOLDITALIC}.DAT{text_style.NONE} file extension.")
    if not len(sys.argv) > 1:
        raise SysArgvError(f"There are no remaining arguments after the verification step.")
    log_info(f"Verification done: {text_style.BOLD}{text_style.PURPLE}{len(sys.argv[1:])}{text_style.NONE}/{text_style.BOLD}{text_style.PURPLE}{initial_count}{text_style.NONE} arguments validated.")