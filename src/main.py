#! /usr/env python3
from pathlib import Path
import sys

from exceptions import SysArgvError, InvalidFileError, format_traceback
from utils import get_energy_unit, validate_arguments
from file_handling import process_file
from logger import log_error
import text_style

def main() -> None:
    # check if energy units must be in electron-Volt or Hartree
    energy_unit = get_energy_unit()

    # Validate the passed arguments before file parsing
    validate_arguments()

    # parse files
    for filepath in sys.argv[1:]:
        try:
            path = Path(filepath)
            process_file(path, energy_unit)
        except InvalidFileError as error:
            log_error(f"{error}")
            continue
        except PermissionError as error:
            log_error(f"Access denied: {text_style.BOLDITALIC}{error.filename}{text_style.NONE}.")
            continue


if __name__ == '__main__':
    print(f"{text_style.BOLD}{text_style.CYAN}[ C23 .DAT -> .CSV ]{text_style.NONE}")
    try:
        main()
    except SysArgvError as error:
        log_error(f"{error}")
    except Exception as error:
        print(f"{text_style.RED}[ UNEXPECTED ERROR - PROGRAM STOPPED ]{text_style.NONE}")
        print(f"{" Traceback (most recent call last) ":=^80}")
        print(format_traceback(error))
        print("=" * 80)
    finally:
        print(f"{text_style.BOLD}{text_style.CYAN}[ FINISHED ]{text_style.NONE}")
