"""
Module for working with git repositories using GitPython

See https://www.devdungeon.com/content/working-git-repositories-python
"""
import socket
from pathlib import Path

import click
import git
from git import exc


class RepoError(Exception):
    """Raised when there is a problem with any aspect of the git repository.

    Attributes:
        message -- explanation of the problem with the repo
    """

    def __init__(self, message):
        self.message = message


def pull_repo(remote_repo: str, local_path: str, update: bool = True) -> str:
    """

    Args:
        remote_repo: Git clone address for the remote repository
        local_path: Path to use for the local clone location
        update: Boolean for whether to pull changes or not

    Returns:

    """
    try:
        r = git.Repo(local_path)
    except (exc.InvalidGitRepositoryError, exc.NoSuchPathError):
        try:
            r = git.Repo.clone_from(remote_repo, local_path)
        except git.exc.GitCommandError as gce:
            err_msg = f"No local clone found and " \
                      f"could not read from remote repository.\n" \
                      f"Repo: {remote_repo},\n" \
                      f"Local clone path: {local_path}"
            raise RepoError(message=err_msg)
            # click.secho(err=True, message=err_msg, fg='red')
            # # click.secho(err=True, message=str(dir(gce)), fg='blue')
            # # click.secho(err=True, message=str(gce.status), fg='green')
            # os.sys.exit(gce.status)

    if update:
        try:
            r.remotes.origin.pull()
        except git.exc.GitCommandError as gce:
            # Log warning and continue with local hint text
            err_msg = f"Could not read from remote repository,\n" \
                      f"Repo: {remote_repo}, \n" \
                      f"Remote: {r.remotes.origin.url}"
            raise RepoError(message=err_msg)
            # click.secho(err=True, message=err_msg, fg='red')

    return local_path


def push_all_changes(local_path):
    repo = git.Repo(local_path)
    if repo.is_dirty(untracked_files=True):
        click.echo(message=f'Changes detected in {local_path}')
        diff = repo.git.diff(repo.head.commit)
        repo.git.add(all=True)
        repo.index.commit(f'Update from {socket.gethostname()}')
        repo.remotes.origin.push()


if __name__ == "__main__":
    local_path = str(Path.home()) + "/.hints.d"
    r = pull_repo('git@github.com:agarthetiger/hints.git', local_path)
    print(str(r))
