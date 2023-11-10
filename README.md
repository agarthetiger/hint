# hint

Hint exists to get help on commands from the command line, without switching context or applications.

## Project status

This product is in nearly daily use by me, and probably me alone. For all intents and purposes this tool is completely unsupported. I make no guarantees about backwards compatibility or commitment to responding to issues or PRs. It is a personal project which I'm happy to share, as open source software licensed with the MIT license if you find it useful and/or want any changes I would suggest forking this repo.

## Installation

Recommended installation method is with [pipx](https://pipxproject.github.io/pipx/).

`pipx install hint-cli`

## Usage

The first time you run `hint TOPIC` it will prompt for configuration values for the following:

* Repository for the hint source - Address of the remote git repository to clone containing your hint content. Use the sample repo from GitHub of `git@github.com:agarthetiger/hint-cli-samples.git` to get started. It is expected that you will create your own content and configure your own repo later. The only topic in the example repo is `bash`. Note that while both the ssh and https clone addresses will work to view content, all functionality to add and modify content will require the ssh style repo address.

Then run `hint TOPIC` where TOPIC is the name of a markdown file in the repository root, without the .md file extension.

eg.

* `hint bash` - Display the formatted contents of https://raw.githubusercontent.com/agarthetiger/hint/trunk/docs/examples/bash.md
* `hint bash curl` - Display only the `curl` subsection from the bash.md file. Valid subsections are any level headings in the markdown document. To display only an H4 subsection, just use the H4 heading text as the 2nd argument.
* `hint --edit bash` - Edit the file bash.md using vim. This requires vim to be installed, the repo to be cloned using ssh, ssh key based authentication to github.com configured for the current user and no restrictions on pushing to the default branch. After an edit, all changes in the locally cloned repository will be added, committed to the local clone and then pushed to GitHub.
* `hint --search pipx` - search for the string pipx as a topic or a string within all topic files.
* `hint --help` - Get help
* `hint --version` - Print the version of hint-cli

## Tab completion for available TOPICs

Tab-completion of TOPICs can be enabled as follows

For Bash, add this to ~/.bashrc:

```bash
eval "$(_HINT_COMPLETE=source_bash hint)"
```

For Zsh, add this to ~/.zshrc:

```bash
eval "$(_HINT_COMPLETE=source_zsh hint)"
```

Open a new shell to enable completion. Or run the eval command directly in your current shell to enable it temporarily.

The above eval examples will invoke your application every time a shell is started. This may slow down shell startup time significantly.

Alternatively, export the generated completion code as a static script to be executed. You can ship this file with your builds; tools like Git do this. At least Zsh will also cache the results of completion files, but not eval scripts.

For Bash:

```bash
_HINT_COMPLETE=source_bash hint > hint-complete.sh
```

For Zsh:

```bash
_HINT_COMPLETE=source_zsh hint > hint-complete.sh
```

In .bashrc or .zshrc, source the script instead of the eval command:

```bash
. /path/to/hint-complete.sh
```

## Upgrading

This project is still in a beta state and as such any version bumps may be breaking until 1.0.0 is released. When upgrading versions prior to v1.0.0 I recommend deleting the config file `~/.hintrc` before running the new version, so that the correct config options are set.

From 1.0.0 onwards, releases will be versioned semantically according to [semver.org 2.0.0](https://semver.org/). Until then, minor version bumps may contain breaking changes.

## Creating content

`hint` is written for you to create your own content, for whatever useful information you would like to access from the command line. It is expected that you will setup your own repository with your own hints.

The repository is expected to contain markdown files with a .md file extension in the root of the repository. Each file name is considered a topic, and each heading a subsection. There is some basic formatting applied to the markdown before being displayed using Click's [echo and style support](https://click.palletsprojects.com/en/7.x/api/?highlight=secho#click.secho).

* Section headings are displayed in bold and cyan.
* Text surrounded by \` characters is displayed in bold and blue.
* All other text is displayed as typed in the markdown file.

Once a repo has been setup and cloned via ssh from GitHub, new pages can be created by running `hint --edit TOPIC` where TOPIC is the name of the file to create. The extension `.md` will be added to the repo automatically and the new file pushed to GitHub after saving and exiting vim.

## Switching hint repositories

Version 0.4.0 changes from using requests to query content directly from GitHub.com to using GitPython to clone the remote repository for the hint content. If you are using hint-cli >=v0.4.0 and want to change the remote repository, update the value for `repo` in `~/.hintrc` and delete the folder `~/.hints.d/hints` and then run hint again.

## Alternatives and comparisons

If you want a tool which pulls community content rather than writing your own, look at [cheat.sh](https://github.com/chubin/cheat.sh). It provides "unified access to the best community driven cheat sheets repositories of the world".

Another tool worth looking at is [How Do I](https://blog.gleitzman.com/post/43330157197/howdoi-instant-coding-answers-via-the-command), with a question and answer format also from the command line.

[Term Cheat](https://github.com/select/term-cheat) is quite a similar tool, with one big list but in a text-based UI which supports searching for the command you want.

[eg](https://github.com/srsudar/eg) is another great tool with a lot of overlap with hint (and more maturity for sure). It has colourised output, a mix of pre-existing community content as well as the option to add your own examples, and a host of configuration possibilities.

[cheat](https://github.com/cheat/cheat) has a wonderful amount of community content ready to go.

Why does hint exist when there are all these other great tools?

* I want to curate my own content. Specifically I don't necessarily want a community-chosen example/answer and I don't want to have to justify what I want as an example in a PR.
* I wanted to be able to access my content from any machine with an internet connection, including but not limited to my work laptop, personal laptop, home lab Raspberry Pi hosts, etc.
* I want to add features I didn't see in any individual existing tool. I have seen almost everything implemented across all the alternative tools out there, and cherry-picked some features for use in hint. Thank you all open-source authors for sharing your ideas.
* I wanted to format the examples on the command line in a specific manner.

... and for completeness,

* When I started this I didn't know some of them existed.
* I wanted to write this myself as a project to continue to learn python so I would have done it anyway.

## System Requirements

* Python >= 3.11
* Pip
* Access to pypi.org or another pip repo with the `hint-cli` python package and dependencies
* Network access to the hints git repository. This may be internet access to GitHub.com but could also be an internal Git server.

## Concept

I use GitHub Pages and MKDocs as well as other Notes applications to collect technical information which I personally find useful. I have a few cheat-sheets with reminders on commands I use regularly but infrequently. The `man` and `info` commands provide help on most commands, however they are very detailed and more useful commands often involve multiple cli tools. Examples bridge the gap between the low level documentation and complex infrequent commands which won't necessarily be in the command history for the current system.

Often I'm using a terminal within PyCharm or VS Code and it's undesirable to switch context to a different application, navigate to a site which may not be open, get the right page and click or scroll to the relevant section. It's not an insurmountable problem, but a workflow which I wanted to optimise.

This tool was inspired in multiple ways by Thomas Stringer's post on [My Personal Wiki … Now Through the Terminal](https://medium.com/@trstringer/my-personal-wiki-now-through-the-terminal-689794e07b42). The fact that I stumbled across this while searching for something else is validation for having a tool and workflow which enables me to remain in the IDE and not switch to a browser. It's similar to taking an alcoholic to a pub and constantly offering them a drink, then saying it's his fault if he ends up drinking. Sure, there is some level of personal responsibility with the alcoholic to resist but a better solution would be to avoid the pub. `hint` keeps me focused, puts the information I need at my fingertips away from distractions.

## Backlog of ideas for improvement

Err, it's vast. My ability to dream up cool things I could add to hint easily outstrips my available time to implement them. The ones I think are worthy of at least writing down will end up on the [project page](https://github.com/agarthetiger/hint/projects/1).

...
