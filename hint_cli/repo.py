"""
Module for working with remote (git) repositories using GitPython

See https://www.devdungeon.com/content/working-git-repositories-python
"""
import os
import socket
from pathlib import Path

import click
import git
from git import exc

LOCAL_PATH = f'{str(Path.home())}/.hints.d/hints'


def get_repo(remote_repo, local_path=LOCAL_PATH, update=True):
    try:
        r = git.Repo(local_path)
    except (exc.InvalidGitRepositoryError, exc.NoSuchPathError):
        try:
            r = git.Repo.clone_from(remote_repo, local_path)
        except git.exc.GitCommandError as gce:
            err_msg = f"Could not read from remote repository and no local clone found,\n" \
                      f"Repo: {remote_repo},\n" \
                      f"Local clone path: {local_path}"
            click.secho(err=True, message=err_msg, fg='red')
            # click.secho(err=True, message=str(dir(gce)), fg='blue')
            # click.secho(err=True, message=str(gce.status), fg='green')
            os.sys.exit(gce.status)

    if update:
        try:
            r.remotes.origin.pull()
        except git.exc.GitCommandError as gce:
            # Log warning and continue with local hint text
            err_msg = f"Could not read from remote repository,\n" \
                      f"Repo: {remote_repo}, \n" \
                      f"Remote: {r.remotes.origin.url}"
            click.secho(err=True, message=err_msg, fg='red')

    return local_path


def push_all_changes():
    repo = git.Repo(LOCAL_PATH)
    if repo.is_dirty(untracked_files=True):
        click.echo(message=f'Changes detected in {LOCAL_PATH}')
        diff = repo.git.diff(repo.head.commit)
        repo.git.add(all=True)
        repo.index.commit(f'Update from {socket.gethostname()}')
        repo.remotes.origin.push()


if __name__ == "__main__":
    r = get_repo('git@github.com:agarthetiger/hints.git')
    print(str(r))
