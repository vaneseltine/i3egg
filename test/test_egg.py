from unittest import mock
import pytest

from i3egg import egg


class TestParseSeconds:
    @pytest.mark.parametrize(
        "incoming, outgoing",
        [("1", 60), ("2", 120), ("3", 180), ("4", 240), ("5", 300)],
    )
    def t_bare_integer_is_minutes(self, incoming, outgoing):
        assert egg.parse_seconds(incoming) == outgoing

    @pytest.mark.parametrize(
        "incoming, outgoing",
        [
            ("1:00", 60),
            ("2:00", 120),
            ("0:1", 1),
            ("0:01", 1),
            ("1:1", 61),
            ("1:60", 120),
        ],
    )
    def t_colon_separator(self, incoming, outgoing):
        assert egg.parse_seconds(incoming) == outgoing

    @pytest.mark.parametrize(
        "incoming, outgoing",
        [
            ("1m00", 60),
            ("2m00", 120),
            ("0m1", 1),
            ("0m01", 1),
            ("1m1", 61),
            ("1m60", 120),
        ],
    )
    def t_minute_separator(self, incoming, outgoing):
        assert egg.parse_seconds(incoming) == outgoing


class TestCLIStuff:

    HELP_CMDS = ["-h", "--help"]
    VERSION_CMDS = ["-V", "--version"]

    @pytest.mark.parametrize("args", ["-h", "--help", "-V", "--version"])
    def t_correctly_skip_following_args(self, args):
        with mock.patch("sys.argv", ["i3egg_test_sysargv"] + args.split()):
            assert egg.check_cli_only()

    @pytest.mark.parametrize("args", HELP_CMDS)
    def t_help_args(self, args, capsys):
        with mock.patch("sys.argv", ["i3egg_test_sysargv"] + args.split()):
            assert egg.check_cli_only()
        captured = capsys.readouterr()
        assert not captured.err
        assert "try" in captured.out.lower()

    @pytest.mark.parametrize("args", VERSION_CMDS)
    def t_version_args(self, args, capsys):
        with mock.patch("sys.argv", ["i3egg_test_sysargv"] + args.split()):
            assert egg.check_cli_only()
        captured = capsys.readouterr()
        assert not captured.err
        assert "egg" in captured.out.lower()
        assert "python" in captured.out.lower()
        assert " at " in captured.out.lower()
