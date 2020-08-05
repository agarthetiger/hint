import click
import re
import requests


RAW_REPO_URL = "https://raw.githubusercontent.com/agarthetiger/mkdocs/master/docs/hints/"
RE_COMMAND = re.compile(r"`(?P<command>.*?)`")

# See available colours listed under click.Style on
# https://click.palletsprojects.com/en/7.x/api/#utilities
TITLE_COLOUR = "cyan"
COMMAND_COLOUR = "blue"


def get_hint_text(topic):
    r = requests.get(f"{RAW_REPO_URL}/{topic}.md")
    r.raise_for_status()
    return r.text


def style_command(match):
    return click.style(match.group('command'), bold=True, fg=COMMAND_COLOUR)


def format_for_stdout(line):
    if line.startswith('#'):
        return '\n' + click.style(line.split(maxsplit=1)[-1],
                                  bold=True, fg=TITLE_COLOUR)
    if line.startswith('*'):
        line = RE_COMMAND.sub(style_command, line.split(maxsplit=1)[-1])
        return '  ' + line
    return line


def print_hint_text(hint_text):
    for line in hint_text.split('\n'):
        # Skip blank lines
        if not line.strip():
            continue

        formatted_line = format_for_stdout(line)
        click.echo(message=formatted_line)


def get_markdown_toc(doc):
    """ Get a dict representing the Table of Contents for a markdown document.

    Args:
        doc: List of strings, each string is a line from the
            markdown document.

    Returns:
        dict:
            Keys are the section heading names
            Values are Tuples with the start and end index of each section,
                including any nested subsections.
    """
    toc = []
    for index, line in enumerate(doc):
        if line.startswith("#"):
            heading = line.split(None, 1)[-1]
            depth = line.index(" ")
            toc.append((heading, depth, index))

    # Process list in reverse order so that when processing each entry you
    # already know the end index for the section.
    toc_dict = {}
    end = {0: len(doc)}

    for section in reversed(toc):
        heading = section[0]
        depth = section[1]
        start_index = section[2]

        # Section (start) index is the end index for that depth section or
        # deeper when traversing the sections in reverse.

        # Find the biggest index which is less than or equal to the depth
        end_index = end[max(key for key in end.keys() if key <= depth)]
        #  Set the new end index for sections of this depth
        end[depth] = start_index
        # Remove end indexes greater than the current depth
        end = {k: v for (k, v) in end.items() if k <= depth}
        toc_dict[heading] = (start_index, end_index)
    return toc_dict


def get_section(hint_text, section):
    hint_text_list = hint_text.split("\n")
    toc = get_markdown_toc(hint_text_list)
    return "\n".join(hint_text_list[toc[section][0]:toc[section][1]])


def get_display_text(hint_text, subsections):
    if len(subsections) == 0:
        return hint_text
    else:
        display_text = ""
        for section in subsections:
            display_text += get_section(hint_text, section)
        if len(display_text) > 0:
            return display_text
        else:
            return hint_text


@click.command()
@click.argument('topic')
@click.argument('subsections', nargs=-1)
def cli(topic, subsections):
    try:
        hint_text = get_hint_text(topic)
    except requests.exceptions.HTTPError as httpe:
        err_msg = f"Could not find remote file for topic '{topic}', " \
                  f"{httpe.response.status_code}, {httpe.request.url}"
        click.secho(err=True, message=err_msg, fg='red')
        return

    display_text = get_display_text(hint_text, subsections)
    print_hint_text(display_text)


if __name__ == "__main__":
    cli()
