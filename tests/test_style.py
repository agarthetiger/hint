import pytest
from hint_cli.style import custom_format

COMMAND = "* `my command` - Some command description"
COMMENT = "// My custom comment format."
NORMAL = "This is just a line of text. Nothing to see here."


def test_custom_format_command_removes_asterisk():
    formatted_line = custom_format(COMMAND)
    assert formatted_line.find('*') == -1

def test_custom_format_command_returns_unmodified_line():
    assert NORMAL == custom_format(NORMAL)

def test_custom_format_command_returns_indented():
    formatted_line = custom_format(COMMAND)
    assert len(formatted_line) > len(COMMAND)
    assert formatted_line.startswith(" ")


@pytest.mark.parametrize("title", [
    "# Title level 1",
    "## Title level 2",
    "### Title level 3",
])
def test_custom_format_title_removes_hashes(title):
    formatted_line = custom_format(title)
    assert formatted_line.find('#') == -1


def test_custom_format_comment_removes_slashes():
    formatted_line = custom_format(COMMENT)
    assert formatted_line.find('/') == -1
