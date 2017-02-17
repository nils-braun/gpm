from git import exc
from git import Repo


class GitRepo:
    def __init__(self, path, allowed_to_create=False):
        self.path = path

        try:
            self.repo = Repo(path)
        except exc.InvalidGitRepositoryError:
            if allowed_to_create:
                self.repo = Repo.init(self.path)
            else:
                raise

        assert not self.repo.bare

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['repo']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self.repo = Repo(self.path)