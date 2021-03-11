# CLI arguments

In order to use hint as I'd like, I want the default behaviour to be to display the hint text for the given topics. If I used sub-commands for edit and search I couldn't use 

`hint python` - should display the python topic text.
`hint python dict` - should display the subsection for dict from the python topic.
`hint edit python` - should edit the python topic.

Using Click sub-commands would require typing a sub-command to display the specified topic. eg `hint display python`. This isn't how I want the cli to work. Therefore I chose to use a single entrypoint and have flags for `-e, --edit` and `-s, --search`. The code is not quite as clean but the functionality requirement is satisfied, which is more important. (Code) readability matters, but not at the expense of functionality.
