from data_objects import DataObject, BandDataObject, DosDataObject
from enums import SpinOrientation, EnergyUnit
from logger import log_write, log_error
from pathlib import Path
from csv import writer as csv_writer
from itertools import zip_longest
import text_style

def get_write_path(path: Path, data_obj: DataObject) -> Path:
    head: str = data_obj.data_type.value
    body: str = "_alpha_" if data_obj.spin == SpinOrientation.Alpha else "_beta_"
    tail: str = "ev.csv" if data_obj.energy_unit == EnergyUnit.ElectronVolt else "ha.csv"
    
    return Path(path.parent).joinpath(f"{head}{body}{tail}")

def get_band_data(path: Path, data_obj: BandDataObject) -> list:
    # format headers for OriginLab
    longnames = ["Fermi"] + ["R-points"] + ["k-points"] + [f"{data_obj.data_type.value}-{i+1}" for i in range(data_obj.y_count)]
    unit = "eV" if data_obj.energy_unit == EnergyUnit.ElectronVolt else "Hartree"
    units = [unit] + ["-"] + ["-"] + [unit for _ in range(data_obj.y_count)]
    comments = ["alpha" if data_obj.spin == SpinOrientation.Alpha else "beta" for _ in range(data_obj.y_count + 3)]
    
    # numerical data
    data = zip_longest([data_obj.fermi_energy], data_obj.kpath_positions, data_obj.x_data, *data_obj.y_data, fillvalue="")

    csv_data = [longnames, units, comments, data]
    return csv_data
    
def get_dos_data(path: Path, data_obj: DosDataObject) -> list:
    # transpose y_data to align columns
    #y_data = list(zip(*data_obj.y_data))

    # format headers for OriginLab
    longnames = ["Fermi Level"] + ["Energy"] + [f"{data_obj.data_type.value}-{i+1}" for i in range(data_obj.y_count - 1)] + [f"{data_obj.data_type.value}-total"]
    unit = "eV" if data_obj.energy_unit == EnergyUnit.ElectronVolt else "Hartree"
    units = [unit] + [unit] + [f"(states/{unit})/cell" for _ in range(data_obj.y_count)]
    comments = ["alpha" if data_obj.spin == SpinOrientation.Alpha else "beta" for _ in range(data_obj.y_count + 2)]
    
    # numerical data
    data = zip_longest([data_obj.fermi_energy], data_obj.x_data, *data_obj.y_data, fillvalue="")

    csv_data = [longnames, units, comments, data]
    return csv_data

def write_csv(path: Path, data_obj: DataObject) -> None:
    if isinstance(data_obj, BandDataObject):
        data = get_band_data(path, data_obj)
    elif isinstance(data_obj, DosDataObject):
        data = get_dos_data(path, data_obj)
    else:
        log_error("Oops")
        return

    csv_file = get_write_path(path, data_obj)
    with open(csv_file, "w", encoding="utf-8", newline="") as file:
        writer = csv_writer(file, delimiter=";")
        for i, row in enumerate(data, 1):
            if i == len(data):
                for subrow in row:
                    writer.writerow(subrow)
            else:
                writer.writerow(row)
    log_write(f"CSV file written: {text_style.BOLDITALIC}{path.name}{text_style.NONE} ({data_obj.spin.name} spin)")

    