import traceback
from pathlib import Path


class SysArgvError(BaseException):
    pass


class InvalidFileError(Exception):
    pass


def format_traceback(exception: BaseException) -> str:
    tb = traceback.TracebackException.from_exception(exception)

    lines = []

    for frame in tb.stack:
        filename = Path(frame.filename).name  # avoid exposing user paths, cleaner output
        lines.append(f'File \033[0;33m"{filename}"\033[0;0m, line \033[0;33m{frame.lineno}\033[0;0m, in \033[0;33m{frame.name}\033[0;0m')
        if frame.line:
            lines.append(f"  \033[0;31m{frame.line.strip()}\033[0;0m")

    exception_name = type(exception).__name__
    lines.append(f"\033[1;35m{exception_name}\033[0;35m: {exception}\033[0;0m")

    return "\n".join(lines)