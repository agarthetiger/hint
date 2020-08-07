# hint

Hint exists to get help on commands from the command line, without switching context or applications. 

## Project status

This is currently a POC project I'm using to see what I find useful and how I want the project to develop. For all intents and purposes this tool is completely unsupported. I make no guarantees about backwards compatibility or commitment to responding to issues or PRs. It is a personal project which I'm happy to share, as open source software licensed with the MIT license if you find it useful and/or want any changes I would suggest forking this repo.    

## Installation

Recommended installation method is with [pipx](https://pipxproject.github.io/pipx/).

`pipx install hint-cli`

## Usage

The first time you run `hint <topic>` it will prompt for configuration values for the following:

* URL for the hint source - Use `https://raw.githubusercontent.com/agarthetiger/hint/trunk/docs/examples/` as an example. It is expected that you will create your own content and add your own url later. The only topic in the example repo is `bash`. Note that this url is the raw url to view just the file contents.
* Personal Auth Token - Enter a GitHub personal auth token if your hints are in a private GitHub repository, otherwise leave blank. 

Then run `hint <topic>` where topic is the name of the markdown file in the repository without the .md file extension.

* `hint bash` - Display the formatted contents of https://raw.githubusercontent.com/agarthetiger/hint/trunk/docs/examples/bash.md 
* `hint bash curl` - Display only the `curl` subsection from the bash.md file. Valid subsections are any level headings in the markdown document. 
* `hint --help` - Get help

## Details

For the first POC this cli will pull information from GitHub from a configurable location and display the contents on the command line. The markdown will be structured using headings which can also be specified. 

`hint` is written for you to create your own content, for whatever useful information you would like to access from the command line. It is expected that you will setup your own repository with your own hints.    

## Alternatives

If you want a tool which pulls community content rather than writing your own, look at [cheat.sh](https://github.com/chubin/cheat.sh). It provides "unified access to the best community driven cheat sheets repositories of the world".  

## Requirements

* User has permissions to install software on the target system.
* System has internet access to github.com

## Concept

I use GitHub Pages and MKDocs as well as other Notes applications to collect technical information which I personally find useful. I have a few cheat-sheets with reminders on commands I use regularly but infrequently. The `man` and `info` commands provide help on most commands, however they are very detailed and more useful commands often involve multiple cli tools. Examples bridge the gap between the low level documentation and complex infrequent commands which won't necessarily be in the command history for the current system. 

Often I'm using a terminal within PyCharm or VS Code and it's undesirable to switch context to a different application, navigate to a site which may not be open, get the right page and click or scroll to the relevant section. It's not an insurmountable problem, but a workflow which I wanted to optimise. 

This tool was inspired in multiple ways by Thomas Stringer's post on [My Personal Wiki … Now Through the Terminal](https://medium.com/@trstringer/my-personal-wiki-now-through-the-terminal-689794e07b42). The fact that I stumbled across this while searching for something else is validation for having a tool and workflow which enables me to remain in the IDE and not switch to a browser. It's similar to taking an alcoholic to a pub and constantly offering them a drink, then saying it's his fault if he ends up drinking. Sure, there is some level of personal responsibility with the alcoholic to resist but a better solution would be to avoid the pub. `hint` keeps me focussed, puts the information I need at my fingertips away from distractions. 
