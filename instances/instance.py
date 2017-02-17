from gpm.utils.git_utils import GitRepo


class Instance:
    def __init__(self):
        pass

    def snapshot(self, db):
        raise NotImplementedError


class ListInstance(Instance):
    def __init__(self, list_of_instances):
        Instance.__init__(self)

        self.list_of_instances = list_of_instances

    def snapshot(self, db):
        from gpm.states.state import ListState
        return ListState([instance.snapshot(db) for instance in self.list_of_instances], db)


class GitInstance(GitRepo, Instance):
    def __init__(self, path):
        GitRepo.__init__(self, path, allowed_to_create=False)
        Instance.__init__(self)

    def snapshot(self, db):
        from gpm.states.state import GitState

        if self.repo.head.is_valid():
            diff = self.repo.git.execute(["git", "diff", "HEAD"])
            return GitState(path=self.path, diff=diff, commit_hash=self.repo.head.commit.hexsha)
        else:
            diff = self.repo.git.execute(["git", "diff"])
            return GitState(path=self.path, diff=diff, commit_hash=None)
