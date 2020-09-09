import glob
import os
import subprocess

import click

from hint_cli import repo, config
from hint_cli.config import get_config
from hint_cli.format import format_for_stdout
from markdown import parser


def print_hint_text(hint_text):
    for line in hint_text.split('\n'):
        # Skip blank lines
        if not line.strip():
            continue
        formatted_line = format_for_stdout(line)
        click.echo(message=formatted_line)


def get_section(hint_text, section):
    hint_text_list = hint_text.split("\n")
    toc = parser.get_toc(hint_text_list)
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


def get_hint_text(git_repo, topic):
    local_path = repo.pull_repo(git_repo, config.REPO_PATH)
    with open(f"{local_path}/{topic}.md", "r") as f:
        text = f.read()
    return text


def edit_hint(topic):
    subprocess.run(['vim', f"{config.REPO_PATH}/{topic}.md"])
    repo.push_all_changes(config.REPO_PATH)


def search_hint(topic):
    msg = ""
    if not topic_exists(topic):
        not_exist = f'Hints for topic "{topic}" not found, run `hint --edit ' \
                    f'{topic}` to create it.'
        msg += click.style(text=not_exist, fg='red')

    return msg


def topic_exists(topic):
    return os.path.isfile(f"{config.REPO_PATH}/{topic}.md")


def get_topics(ctx, args, incomplete):
    return [filename.split('/')[-1][0:-3]
            for filename in glob.glob(f"{config.REPO_PATH}/{incomplete}*.md")]


@click.command()
@click.option('-e', '--edit', is_flag=True)
@click.option('-s', '--search', is_flag=True)
@click.argument('topic', autocompletion=get_topics)
@click.argument('subsections', nargs=-1)
@click.version_option()
def cli(edit, search, topic, subsections):
    conf = get_config()
    if edit:
        edit_hint(topic=topic)
    elif search or not topic_exists(topic):
        print_hint_text(search_hint(topic=topic))
    else:
        hint_text = get_hint_text(git_repo=conf['hint']['repo'], topic=topic)
        display_text = get_display_text(hint_text, subsections)
        print_hint_text(display_text)
