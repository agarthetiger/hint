import subprocess
import click

from hint_cli import repo
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
    local_path = repo.get_repo(git_repo)
    with open(f"{local_path}/{topic}.md", "r") as f:
        text = f.read()
    return text


def edit_hint(topic):
    subprocess.run(['vim', f"{repo.LOCAL_PATH}/{topic}.md"])
    repo.push_all_changes()


@click.command()
@click.option('-e', '--edit', is_flag=True)
@click.argument('topic')
@click.argument('subsections', nargs=-1)
@click.version_option()
def cli(edit, topic, subsections):
    conf = get_config()
    if edit:
        edit_hint(topic=topic)
    else:
        try:
            hint_text = get_hint_text(git_repo=conf['hint']['repo'], topic=topic)
        except FileNotFoundError:
            fnf_msg = f'Hints for topic "{topic}" not found, run `hint --edit {topic}` to create it.'
            click.secho(err=True, message=fnf_msg, fg='red')
            return
        display_text = get_display_text(hint_text, subsections)
        print_hint_text(display_text)
