from pprint import pprint

from markdown.parser import get_toc

markdown_doc = '''# Title

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

test_doc = markdown_doc.split('\n')


def test_get_toc_returns_whole_doc():
    toc = get_toc(doc=test_doc)
    assert 'title' in toc.keys()
    assert toc['title'].start == 0
    assert toc['title'].end == len(test_doc)


def test_get_toc_returns_first_heading():
    toc = get_toc(doc=test_doc)
    assert 'dictionary' in toc.keys()
    assert toc['dictionary'].start == 2
    assert toc['dictionary'].end == toc['lists'].start


def test_get_doc_returns_section_including_nested_headings():
    toc = get_toc(doc=test_doc)
    assert 'lists' in toc.keys()
    assert toc['lists'].start == toc['dictionary'].end
    assert toc['lists'].end == len(test_doc)
