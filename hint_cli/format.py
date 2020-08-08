import re

import click

RE_COMMAND = re.compile(r"`(?P<command>.*?)`")

# See available colours listed under click.Style on
# https://click.palletsprojects.com/en/7.x/api/#utilities
TITLE_COLOUR = "cyan"
COMMAND_COLOUR = "blue"


def style_command(match):
    return click.style(match.group('command'), bold=True, fg=COMMAND_COLOUR)


def format_for_stdout(line):
    if line.startswith('#'):
        return click.style(line.split(maxsplit=1)[-1], bold=True, fg=TITLE_COLOUR)
    if line.startswith('*'):
        line = RE_COMMAND.sub(style_command, line.split(maxsplit=1)[-1])
        return '  ' + line
    return line
