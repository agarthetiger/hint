import configparser
import os
import sys
from pathlib import Path

import click

HOME = str(Path.home())
CONFIG_FILE = f"{HOME}/.hintrc"
REPO_PATH = f"{HOME}/.hints.d/"


def create_config():
    config = configparser.ConfigParser()
    try:
        with open(CONFIG_FILE, 'w') as configfile:
            config['hint'] = {}
            config['hint']['repo'] = input("Git repository to clone for the hint source:")
            # config['hint']['token'] = input(
            #     "Personal Auth Token for private repos:")
            config.write(configfile)
    except IOError:
        err_msg = f"Cannot create config file {CONFIG_FILE}"
        click.secho(err=True, message=err_msg, fg='red')
        sys.exit(1)
    return config


def validate_config(config):
    # TODO add code to validate the expected configuration here
    pass


def get_config():
    if os.path.isfile(CONFIG_FILE):
        # Read in the config file if it exists
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
    else:
        # otherwise create a config file
        config = create_config()

    validate_config(config)
    return config
