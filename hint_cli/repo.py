"""
Module for working with git repositories using GitPython

See https://www.devdungeon.com/content/working-git-repositories-python
"""
import socket
from pathlib import Path

import click
import git


class RepoError(Exception):
    """Raised when there is a problem with any aspect of the git repository.

    Attributes:
        message -- explanation of the problem with the repo
    """

    def __init__(self, message):
        self.message = message


def pull(local_path: str) -> bool:
    """Pull changes from a remote repo. Requires a local repo clone to already
    exist.

    Args:
        local_path: Path to use for the local clone location

    Returns:


    Raises:
        RepoError:
    """
    try:
        r = git.Repo(local_path)
    except git.exc.InvalidGitRepositoryError:
        raise RepoError(message=f"Caught InvalidGitRepositoryError, is {local_path} a git clone?")
    except git.exc.NoSuchPathError:
        return clone(local_path)

    try:
        r.remotes.origin.pull()
    except git.exc.GitCommandError as gce:
        # Log warning and continue with local hint text
        err_msg = f"Could not read from remote repository,\n" \
                  f"Remote: {r.remotes.origin.url}"
        raise RepoError(message=err_msg)
        # click.secho(err=True, message=err_msg, fg='red')

    return True


def clone(local_path: str):
    # Prompt for remote repo location. One time operation per install.
    repo_url = click.prompt('Please enter the https url for your hints repository: ')
    try:
        git.Repo.clone_from(repo_url, local_path)
    except git.exc.GitCommandError as gce:
        err_msg = f"No local clone found and " \
                  f"could not read from remote repository.\n" \
                  f"Repo: {repo_url},\n" \
                  f"Local clone path: {local_path}"
        raise RepoError(message=err_msg)
        # click.secho(err=True, message=err_msg, fg='red')
        # # click.secho(err=True, message=str(dir(gce)), fg='blue')
        # # click.secho(err=True, message=str(gce.status), fg='green')
        # os.sys.exit(gce.status)
    return True


def push(local_path):
    repo = git.Repo(local_path)
    if repo.is_dirty(untracked_files=True):
        click.echo(message=f'Changes detected in {local_path}')
        diff = repo.git.diff(repo.head.commit)
        repo.git.add(all=True)
        repo.index.commit(f'Update from {socket.gethostname()}')
        try:
            repo.remotes.origin.push()
        except git.exc.GitCommandError as gce:
            # Log warning and continue with local hint text
            err_msg = f"Error pushing to remote repository,\n" \
                      f"Remote: {repo.remotes.origin.url}"
            raise RepoError(message=err_msg)


if __name__ == "__main__":
    path = str(Path.home()) + "/.hints.d"
    test_repo = pull(local_path=path)
    print(str(test_repo))
