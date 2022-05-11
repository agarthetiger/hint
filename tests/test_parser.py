import pytest
from hint_cli.parser import get_toc

markdown = '''# Title

## dictionary

Here is some information about python dicts.

```python
nfl_teams = {'seattle': 'seahawks', 'chicago': 'bears'}
```

## Lists

Here is some text about lists.

### List Comprehensions

```python
cities_with_nfl_teams = [city for city, team in nfl_teams.items()]
```
'''


@pytest.fixture
def markdown_doc():
    return markdown


@pytest.fixture
def markdown_lines():
    return markdown.split('\n')


def test_get_toc_returns_whole_doc(markdown_lines):
    toc = get_toc(doc=markdown_lines)
    assert 'title' in toc.keys()
    assert toc['title'].start == 0
    assert toc['title'].end == len(markdown_lines)


def test_get_toc_returns_first_heading(markdown_lines):
    toc = get_toc(doc=markdown_lines)
    assert 'dictionary' in toc.keys()
    assert toc['dictionary'].start == 2
    assert toc['dictionary'].end == toc['lists'].start


def test_get_doc_returns_section_including_nested_headings(markdown_lines):
    toc = get_toc(doc=markdown_lines)
    assert 'lists' in toc.keys()
    assert toc['lists'].start == toc['dictionary'].end
    assert toc['lists'].end == len(markdown_lines)
