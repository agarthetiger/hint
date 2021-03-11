from pygments import highlight
from pygments.style import Style
from pygments.token import Token
from pygments.lexers.markup import MarkdownLexer
from pygments.formatters import Terminal256Formatter


code = '''
# Title

Blah blah blah

## Second level title

Another paragraph and a list, here it comes

* ```shell command``` Command explanation
* ```shell another command``` And another explanation, well, what did you expect?

### and a third

```python
print("Hello World")
```

'''
result = highlight(code, MarkdownLexer(), Terminal256Formatter())
print(result)
