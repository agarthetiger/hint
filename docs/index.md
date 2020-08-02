---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: Home
permalink: /
---
Hint exists to get help on commands from the command line, without switching context or applications. 

## Project status

This is currently a POC project I'm using to see what I find useful and how I want the project to develop. For all intents and purposes this tool is completely unsupported. I make no guarantees about backwards compatibility or commitment to responding to issues or PRs. It is a personal project which I'm happy to share, as open source software licensed with the MIT license if you find it useful and/or want any changes I would suggest forking this repo.    

## Details

For the first POC this cli will pull information from GitHub from a fixed repository, branch and folder and display the contents on the command line. The markdown will be structured using headings which can also be specified. 

## Installation

TBC once published on pypi.org. 

Recommended installation method is with [pipx](https://pipxproject.github.io/pipx/).

## Usage

`hint bash` - Output the contents of https://raw.githubusercontent.com/agarthetiger/mkdocs/master/docs/hints/bash.md
 
`hint --help` - Show help text

## Requirements

* User has permissions to install software on the target system.
* System has internet access to github.com

## Concept

I use GitHub Pages and MKDocs to collect notes and technical information which I personally find useful. I have a few cheat-sheets with reminders on commands I use regularly but infrequently. The `man` and `info` commands provide help on most commands, however they are very detailed and more useful commands often involve multiple cli tools. Examples bridge the gap between the low level documentation and complex infrequent commands which won't necessarily be in the command history for the current system. 

Often I'm using a terminal within PyCharm or VS Code and it's undesirable to switch context to a different application, navigate to a site which may not be open, get the right page and click or scroll to the relevant section. It's not an insurmountable problem, but a workflow which I wanted to optimise. 

This tool was inspired in multiple ways by Thomas Stringer's post on [My Personal Wiki … Now Through the Terminal](https://medium.com/@trstringer/my-personal-wiki-now-through-the-terminal-689794e07b42). The fact that I stumbled across this while searching for something else is validation for having a tool and workflow which enables me to remain in the IDE and not switch to a browser. It's similar to taking an alcoholic to a pub and constantly offering them a drink, then saying it's his fault if he ends up drinking. Sure, there is some level of personal responsibility with the alcoholic to resist but a better solution would be to avoid the pub. I want to avoid switching to my browser and all it's associated tabs. I even want to avoid having to switch past other open applications which may also have work pending. I just want the right content delivered to the right place at the right time, and this is what I aim to achieve with hint.

## Backlog of ideas for improvement

Err, it's vast. My ability to dream up cool things I could add to hint easily outstrips my free time to implement them. The ones I think are worthy of at least writing down will end up on the [project page](https://github.com/agarthetiger/hint/projects/1).

