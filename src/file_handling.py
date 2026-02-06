from pathlib import Path

from data_objects import DataObject, DataObjectType
from enums import EnergyUnit
from exceptions import InvalidFileError
from file_parsing import FileParser, BandFileParser, DosFileParser
from utils import iter_lines
from logger import log_read
from csv_writter import write_csv
import text_style


def parse_file(path: Path, parser: FileParser) -> list[DataObject]:
    for line in iter_lines(path):
        parser.feed(line)
    
    return parser.build()

def load_file(path: Path, energy_unit: EnergyUnit) -> list[DataObject]:
    PARSER_MAP = {
        "band": (BandFileParser, DataObjectType.Band),
        "doss": (DosFileParser, DataObjectType.DOS),
        "cohp": (DosFileParser, DataObjectType.COHP),
        "coop": (DosFileParser, DataObjectType.COOP),
    }
    lower = path.name.lower()
    for key, (parser_class, data_type) in PARSER_MAP.items():
        if key in lower:
            return parse_file(path, parser_class(energy_unit, data_type))
    # Should never get here, but is a fail safe
    raise InvalidFileError("Could not attribute the parser to this file.")

def process_file(path: Path, energy_unit: EnergyUnit) -> None:
    log_read(f"{text_style.BOLDITALIC}{path.name}{text_style.NONE}\n         from: {text_style.ITALIC}{path.absolute().parent}{text_style.NONE}")
    data_objs = load_file(path, energy_unit)
    for data_obj in data_objs:
        write_csv(path, data_obj)