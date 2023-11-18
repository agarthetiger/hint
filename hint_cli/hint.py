import glob
import os
import logging
import re
import subprocess
from pathlib import Path

import click

from pygments import highlight
from pygments import lexers
from pygments.formatters import Terminal256Formatter

from hint_cli import repo, parser, style

logger = logging.getLogger(__name__)
conf = None
HOME = str(Path.home())
CONFIG_FILE = f"{HOME}/.hintrc"
LOCAL_PATH = f"{HOME}/.hints.d/hints"
# See https://pygments.org/styles/ for available styles
CODE_STYLE = "native"


def print_to_console(hint_text: str):
    global CODE_STYLE

    formatted_lines = ""
    code_block_lines = ""
    in_code_block = False
    code_lang = ""

    for line in hint_text.split('\n'):
        if line.strip().startswith('```') or in_code_block:
            match = re.findall(r'```(\w+)', line.strip())
            if match:
                # First line of code block
                in_code_block = True
                code_lang = match[0]
            elif line.strip().startswith('```'):
                # Last line of code block
                in_code_block = False
                click.echo(message=highlight(code=code_block_lines,
                    lexer=lexers.get_lexer_by_name(code_lang),
                    formatter=Terminal256Formatter(style=CODE_STYLE)))
            else:
                code_block_lines += line + '\n'
        elif line.strip():
            click.echo(message=style.custom_format(line=line.strip()))
        else:
            continue


def get_section(hint_text: str, section: str):
    """
    Return a section of text based on the section heading from the
    hint_text string. '\n' delimited string containing a markdown document.

    Args:
        hint_text (str): '\n' delimited string containing a markdown document.
        section (str): Section heading to search the hint_text for.

    Returns:
        str: Either the section of text from the hint_text with the
            section heading or an error message indicating the section
            could not be found.
    """
    hint_text_list = hint_text.split("\n")
    section = section.lower()
    toc = parser.get_toc(hint_text_list)
    try:
        return "\n".join(hint_text_list[toc[section].start:toc[section].end])
    except KeyError:
        return f"Section '{section}' not found in document."


def get_display_text(hint_text, subsections):
    """
    Get the requested sections of text from the hint_text document.

    Args:
        hint_text (str): Hint text to display
        subsections (tuple): Optional section(s) to return instead of
            the whole document.

    Returns:
        str: Text to display from the hint_text argument.
    """
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


def get_topic_from_repo(topic: str) -> str:
    """
    Get the topic text from the git repository.

    Args:
        topic: Name of the topic to retrieve the contents for.

    Returns:
        str: String with the contents of the file. '\n' line delimiters
    """
    repo.pull(local_path=LOCAL_PATH)
    with open(f"{LOCAL_PATH}/{topic}.md", "r") as f:
        text = f.read()
    return text


def cmd_edit_topic(topic: str, offline: bool) -> None:
    """
    Creates or edits a markdown file with the name of the topic.

    Args:
        topic: Name of the topic to create or edit.
        offline: If offline, skip or ignore methods and errors due to lack of
            network connectivity.
    """
    if not offline:
        repo.pull(local_path=LOCAL_PATH)

    subprocess.run(['vim', f"{LOCAL_PATH}/{topic}.md"])

    if not offline:
        repo.push(LOCAL_PATH)


def search_for_text_in_topics(search_term: str):
    """
    Search for the requested text in all the hint topic files.

    Args:
        search_term (str): String to search in the topic files for.

    Returns:
        String message containing details of the files and the
            lines containing the matches.
    """
    msg = ""
    for topic_file in glob.glob(f"{LOCAL_PATH}/*.md"):
        with open(topic_file) as file:
            matches = [line
                       for line in file.readlines()
                       if search_term.lower() in line.lower()]
        if len(matches) > 0:
            msg += f"// Matches found in {topic_file}\n"
            for match in matches:
                msg += f"{match}\n"
    return msg


def cmd_search_for_topic(topic: str, offline: bool):
    """
    Check if the topic (file) exists. Topics are files in a locally
    cloned git repository. The topic name should match a markdown
    file with a .md file extension. Future versions may fuzzy-match
    the filename, or search other locations such as a remote GitHub
    repository.

    The folder this methods uses to check for the file is defined
    by `config.REPO_PATH`
    Args:
        topic: Name of the topic to verify exists.
        offline: If offline, skip or ignore methods and errors due to lack of
            network connectivity.

    Returns:
        bool: True if topic (file) exists, otherwise False.
    """

    if not offline:
        repo.pull(local_path=LOCAL_PATH)

    if os.path.isfile(f"{LOCAL_PATH}/{topic}.md"):
        msg = f'// Hint found for `{topic}`.\n'
    else:
        msg = f'// Hints for topic "{topic}" not found, run `hint --edit ' \
              f'{topic}` to create it.\n'
    msg += search_for_text_in_topics(topic)

    print_to_console(msg)


def cmd_display_topic(topic: str, subsections: tuple, offline: bool):
    """
    Display the hint topic to the console. If there are no subsections
    specified, display the whole file, otherwise just display the
    subsections from the topic.

    Args:
        topic (str): Name of the topic to display
        offline: If offline, skip or ignore methods and errors due to lack of
            network connectivity.
        subsections (tuple): Optional subsections to display from the
            specified topic.

    Returns:
        Nothing. Correct function is to print text to the console.
    """
    # If no other flags passed, display the hint topic [and subsections]

    global LOCAL_PATH
    if not offline:
        repo.pull(local_path=LOCAL_PATH)

    # Create a list of all files and check for a lowercase match, so we can open hint files with a different case for the filename.
    hints = os.listdir(LOCAL_PATH)
    for hint in hints:
        name, extension = os.path.splitext(hint)
        if name.lower() == topic.lower() and extension == ".md":
            # Replace the topic with the potentially cased filename to open.
            topic = name
            break
    else:
        click.secho(message=f"Could not find topic file {topic}.md in {LOCAL_PATH}, searching instead...", err=True, fg="red")
        cmd_search_for_topic(topic=topic, offline=offline)
        return

    # if not os.path.isfile(f"{LOCAL_PATH}/{topic}.md"):
    #     click.secho(message=f"Could not find topic file {topic}.md in {LOCAL_PATH}.", err=True, fg="red")
    #     os.sys.exit(1)
    full_hint_text = get_topic_from_repo(topic=topic)
    display_text = get_display_text(full_hint_text, subsections)
    print_to_console(display_text)


# noinspection PyUnusedLocal
def _get_topics(ctx, param, incomplete):
    """
    Callback function for Click command-line auto-completion.
    This allows tab-completion of existing hint topics.
    See https://click.palletsprojects.com/en/8.1.x/shell-completion/#overriding-value-completion

    Returns:
        (list): Filenames matching the incomplete arg value.
    """
    print(f"autocompleting...")
    return [str(filename.split('/')[-1][0:-3])
            for filename in glob.glob(f"{LOCAL_PATH}/{incomplete}*.md")]


@click.command()
@click.option('-e', '--edit', is_flag=True)
@click.option('-o', '--offline', is_flag=True)
@click.option('-s', '--search', is_flag=True)
@click.argument('topic', shell_complete=_get_topics)
@click.argument('subsections', nargs=-1)
@click.version_option()
def cli_entrypoint(edit, offline, search, topic, subsections):
    """
    CLI entrypoint.

    Args:
        edit (bool): True if the topic should be edited. Will be
            created if it does not exist.
        offline (bool): True if we should skip or ignore methods and
            errors due to network connectivity.
        search (bool): True if the topic string should be searched for.
            Search will first look for filename matches, and if not found
            all the files contents will be searched instead.
        topic (string): Name of the topic to create, edit or search for.
        subsections (tuple): Optional sub-sections to display. Only valid
            for the (default) display action.

    Returns:
        Non-zero exit code on failure, otherwise correct operation
        is to print output to the console.
    """
    if edit:
        cmd_edit_topic(topic=topic, offline=offline)
    elif search:
        cmd_search_for_topic(topic=topic, offline=offline)
    else:
        cmd_display_topic(topic=topic, subsections=subsections, offline=offline)
