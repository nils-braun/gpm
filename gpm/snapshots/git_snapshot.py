from git import Repo

from gpm.snapshots.base import BaseSnapshot


class GitSnapshot(BaseSnapshot):
    def __init__(self, path):
        BaseSnapshot.__init__(self)

        self.path = path

        git_repo = Repo(path)

        self.diff = git_repo.git.execute(["git", "diff", "HEAD"])
        self.commit_hash = git_repo.head.commit.hexsha

    @property
    def name_param(self):
        return self.path

    def __eq__(self, other):
        return (other.path == self.path and
                other.diff == self.diff and
                other.commit_hash == self.commit_hash)