from unittest.mock import patch

from hint_cli.hint import print_to_console


@patch('hint_cli.hint.style')
@patch('hint_cli.hint.click')
def test_get_topics_returns_list(mock_click, mock_style):
    test_string = "Test string"
    print(mock_click)
    print(mock_style)
    def return_same(line: str): return line
    mock_style.custom_format.side_effect = return_same
    print_to_console(test_string)
    mock_style.custom_format.assert_called_with(line=test_string)
    mock_click.echo.assert_called_with(message=test_string)
