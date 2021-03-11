import glob
import os
import logging
import subprocess

import click
from rich.console import Console
from rich.markdown import Markdown

from hint_cli import repo, config_manager
from hint_cli.format import format_for_stdout
from markdown import parser


logger = logging.getLogger(__name__)
conf = None


def print_markdown(hint_markdown):
    console = Console()
    md = Markdown(hint_markdown)
    console.print(md)


def print_to_console(hint_text: str):
    for line in hint_text.split('\n'):
        # Skip blank lines
        if not line.strip():
            continue
        formatted_line = format_for_stdout(line)
        click.echo(message=formatted_line)


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


def get_topic_from_repo(git_repo: str, topic: str):
    """
    Get the topic text from the git repository.

    Args:
        git_repo:
        topic:

    Returns:

    """
    local_path = repo.pull_repo(remote_repo=git_repo, local_path=config_manager.REPO_PATH)
    with open(f"{local_path}/{topic}.md", "r") as f:
        text = f.read()
    return text


def create_or_edit_topic(topic: str):
    """
    Creates or edits a markdown file with the name of the topic.

    Args:
        topic: Name of the topic to create or edit.
    """
    subprocess.run(['vim', f"{config_manager.REPO_PATH}/{topic}.md"])
    repo.push_all_changes(config_manager.REPO_PATH)


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
    for topic_file in glob.glob(f"{config_manager.REPO_PATH}/*.md"):
        with open(topic_file) as file:
            matches = [line
                       for line in file.readlines()
                       if line.find(search_term) != -1]
        if len(matches) > 0:
            msg += f"Matches found in {topic_file}\n"
            for match in matches:
                msg += f"{match}\n"
    return msg


def search_for_topic(topic: str):
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

    Returns:
        bool: True if topic (file) exists, otherwise False.
    """
    msg = ""
    if os.path.isfile(f"{config_manager.REPO_PATH}/{topic}.md"):
        msg = f'Hint found for `{topic}`.\n'
    else:
        msg = f'Hints for topic "{topic}" not found, run `hint --edit ' \
              f'{topic}` to create it.\n'
    msg += search_for_text_in_topics(topic)

    print_to_console(msg)


def display_topic(topic: str, subsections: tuple):
    """
    Display the hint topic to the console. If there are no subsections
    specified, display the whole file, otherwise just display the
    subsections from the topic.

    Args:
        topic (str): Name of the topic to display
        subsections (tuple): Optional subsections to display from the
            specified topic.

    Returns:
        Nothing. Correct function is to print text to the console.
    """
    # If no other flags passed, display the hint topic [and subsections]
    full_hint_text = get_topic_from_repo(git_repo=conf['hint']['repo'], topic=topic)
    display_text = get_display_text(full_hint_text, subsections)
    print_to_console(display_text)


def _get_topics(ctx, args, incomplete: str):
    """
    Callback function for Click command-line auto-completion.
    This allows tab-completion of existing hint topics.
    See https://click.palletsprojects.com/en/7.x/bashcomplete/?#what-it-completes

    Returns:
        (list): Filenames matching the incomplete arg value.
    """
    return [filename.split('/')[-1][0:-3]
            for filename in glob.glob(f"{config_manager.REPO_PATH}/{incomplete}*.md")]


@click.command()
@click.option('-e', '--edit', is_flag=True)
@click.option('-s', '--search', is_flag=True)
@click.argument('topic', autocompletion=_get_topics)
@click.argument('subsections', nargs=-1)
@click.version_option()
def cli(edit, search, topic, subsections):
    """
    CLI entrypoint.

    Args:
        edit (bool): True if the topic should be edited. Will be
            created if it does not exist.
        search (bool): True if the topic string should be searched for.
            Search will first look for filename matches, and if not found
            the file contents will be searched instead.
        topic (string): Name of the topic to create, update or search for.
        subsections (tuple): Optional sub-sections to display. Only valid
            for the (default) display action.

    Returns:
        Non-zero exit code on failure, otherwise correct operation
        is to print output to the console.
    """
    global conf
    conf = config_manager.get_config()
    if edit:
        create_or_edit_topic(topic=topic)
    elif search:
        search_for_topic(topic=topic)
    else:
        display_topic(topic=topic, subsections=subsections)
