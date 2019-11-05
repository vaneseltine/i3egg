"""A very simple timer for i3"""
import re
import subprocess
import sys
import time

FONT = "pango:LuxiMono 18"


def main() -> None:
    """A very simple timer for i3"""
    raw_input = input_from_args() or input_from_i3()
    seconds = parse_seconds(raw_input)
    print(f"{seconds} sec...")
    time.sleep(seconds)
    notify_complete(seconds)


def input_from_args():
    """
    Get min/sec input from the command line arguments.
    """
    args = sys.argv[1:]
    return " ".join(args)


def input_from_i3() -> str:
    """
    Get min/sec input from an i3 input box.
    """
    full_output = subprocess.getoutput(f"i3-input -f {FONT} -P 'Minutes: '")
    input_lines = full_output.splitlines()
    key_line: str = [s for s in input_lines if s.startswith("output")][-1]
    return key_line.split(" = ")[-1]


def parse_seconds(raw_input: str, divider: str = r"[^\d]+") -> int:
    """
    Convert a string like '1:30', '3', or '4m3' into seconds (90; 180; 243).
    """
    try:
        return int(raw_input) * 60
    except ValueError:
        pass
    mins, secs = re.split(divider, raw_input)
    return int(mins) * 60 + int(secs)


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
