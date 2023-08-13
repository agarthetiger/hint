import re
import click


RE_COMMAND = re.compile(r"`(?P<command>.*?)`")

# See available colours listed under click.Style on
# https://click.palletsprojects.com/en/7.x/api/#utilities
TITLE_COLOUR = "cyan"
COMMAND_COLOUR = "blue"
COMMENT_COLOUR = "green"


def style_title(text: str) -> str:
    return click.style(text, bold=True, fg=TITLE_COLOUR)


def style_command(match):
    return click.style(match.group('command'), bold=True, fg=COMMAND_COLOUR)


def style_comment(text: str) -> str:
    return click.style(text, bold=True, fg=COMMENT_COLOUR)


def style_default(text: str) -> str:
    return RE_COMMAND.sub(style_command, text)


def custom_format(line: str) -> str:
    """Apply custom formatting in addition to the regular markdown.

    Args:
        line: Line of text to apply formatting to. The line may or may not
            contain any characters which require additional formatting.

    Returns:
        str: The formatted text string for display
    """

    # click.echo(f"Checking line '{line}'")
    if line.startswith('#'):
        return style_title(line.split(maxsplit=1)[-1])
    elif line.startswith('*'):
        line = RE_COMMAND.sub(style_command, line.split(maxsplit=1)[-1])
        return '  ' + line
    elif line.startswith('//'):
        line = style_comment(line.split(maxsplit=1)[-1])
    else:
        line = style_default(line)
        pass

    return line
