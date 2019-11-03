import subprocess
import time
import typing as T
import sys

FONT = "pango:LuxiMono 18"


def get_input_from_i3() -> str:
    full_output = subprocess.getoutput(f"i3-input -f {FONT} -P 'Minutes: '")
    line: str = [s for s in full_output.splitlines() if s.startswith("output")][-1]
    return line.split(" = ")[-1]


def parse_seconds(raw_input: str, divider: str = ":") -> int:
    try:
        return int(raw_input) * 60
    except ValueError:
        pass
    mins, secs = [int(x) for x in raw_input.split(divider)]
    return mins * 60 + secs


def notify_complete(seconds: int) -> None:
    minutes, seconds = divmod(seconds, 60)
    print("DING DING DING")
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


def main() -> None:
    input_args = " ".join(sys.argv[1:])
    raw_input = input_args or get_input_from_i3()
    seconds = parse_seconds(raw_input)
    print(f"{seconds} sec...")
    time.sleep(seconds)
    notify_complete(seconds)


if __name__ == "__main__":
    main()
