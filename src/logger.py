from enum import Enum
import text_style


class LogLevel(Enum):
    Info = 0
    Read = 1
    Write = 2
    Warning = 3
    Error = 4


def log(level: LogLevel, message: str) -> None:
    match level:
        case LogLevel.Info:
            log = f"{text_style.BOLD}{text_style.WHITE}[ INFO ]"
        case LogLevel.Read:
            log = f"{text_style.BOLD}{text_style.BLUE}[ READ ]"
        case LogLevel.Write:
            log = f"{text_style.BOLD}{text_style.GREEN}[ DONE ]"
        case LogLevel.Warning:
            log = f"{text_style.BOLD}{text_style.YELLOW}[ WARNING ]"
        case LogLevel.Error:
            log = f"{text_style.BOLD}{text_style.RED}[ ERROR ]"
    log += f"{text_style.NONE} "
    log += message
    print(log)

def log_info(message: str) -> None:
    return log(LogLevel.Info, message)

def log_read(message: str) -> None:
    return log(LogLevel.Read, message)

def log_write(message: str) -> None:
    return log(LogLevel.Write, message)

def log_error(message: str) -> None:
    return log(LogLevel.Error, message)

def log_warn(message: str) -> None:
    return log(LogLevel.Warning, message)