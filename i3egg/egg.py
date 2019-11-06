"""An overly simple timer for i3."""
import re
import subprocess
import sys
import time
import typing as T
from pathlib import Path

__version__ = "0.9.3"

FONT = "pango:LuxiMono 18"
DEFAULT_DIVIDER = re.compile(r"[^\d]+")

UserInput = str


def main() -> int:
    """An overly simple timer for i3."""
    if check_cli_only():
        return 0
    raw_input = input_from_args() or input_from_i3()
    seconds = parse_seconds(raw_input)
    wait_seconds(seconds)
    notify_complete(seconds)
    return 0


def check_cli_only() -> bool:
    args = sys.argv[1:]
    if "-V" in args or "--version" in args:
        report_version()
        return True
    if "-h" in args or "--help" in args:
        report_help()
        return True
    return False


def report_version() -> None:
    egg_version = f"i3egg {__version__} at {Path(__file__).parent.absolute()}"
    py_version = f"Python {sys.version.split(' ')[0]} at {sys.executable}"
    print(f"{egg_version}\n{py_version}")


def report_help() -> None:
    print("Try: i3egg 0:02")


def input_from_args() -> UserInput:
    """
    Get min/sec input from the command line arguments.
    """
    args = sys.argv[1:]
    command_line_input: UserInput = " ".join(args)
    return command_line_input


def input_from_i3() -> UserInput:
    """
    Get min/sec input from an i3 input box.
    """
    full_output = subprocess.getoutput(f"i3-input -f {FONT} -P 'Minutes: '")
    input_lines = full_output.splitlines()
    key_line: str = [s for s in input_lines if s.startswith("output")][-1]
    i3_input: UserInput = key_line.split(" = ")[-1]
    return i3_input


def parse_seconds(
    raw_input: UserInput, divider: T.Pattern[str] = DEFAULT_DIVIDER
) -> int:
    """
    Convert a string like '1:30', '3', or '4m3' into seconds (90; 180; 243).
    """
    try:
        return int(raw_input) * 60
    except ValueError:
        pass
    mins, secs = divider.split(raw_input)
    return int(mins or 0) * 60 + int(secs or 0)


def wait_seconds(seconds: int) -> None:
    print(f"{seconds} sec...")
    time.sleep(seconds)


def notify_complete(seconds: int) -> None:
    """
    Call i3-nagbar to report the end of the timer.
    """
    minutes, seconds = divmod(seconds, 60)
    subprocess.check_call(
        [
            "i3-nagbar",
            "-t",
            "warning",
            "-f",
            FONT,
            f"-m i3egg: {minutes}m {seconds}s timer has expired.",
        ]
    )


if __name__ == "__main__":
    main()
