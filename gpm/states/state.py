from gpm.utils.git_utils import GitRepo

from tempfile import NamedTemporaryFile

class State:
    def __init__(self):
        pass

    def apply(self, instance, db):
        raise NotImplementedError

    def complete_loading(self, db):
        pass

    def store(self, db):
        key_to_store = db.set(self)

        return key_to_store

    @staticmethod
    def load(db, key):
        stored_state = db.get(key)

        assert isinstance(stored_state, State)

        stored_state.complete_loading(db)

        return stored_state


class ListState(State):
    def __init__(self, list_of_states, db):
        State.__init__(self)

        self.keys = []
        self.list_of_states = list_of_states

        for state in list_of_states:
            key = state.store(db)

            self.keys.append(key)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['list_of_states']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __iter__(self):
        return iter(self.list_of_states)

    def apply(self, instance, db):
        from gpm.instances.instance import ListInstance
        assert isinstance(instance, ListInstance)

        assert len(self.list_of_states) == len(instance.list_of_instances)

        for state, instance in zip(self.list_of_states, instance.list_of_instances):
            state.apply(instance, db)

    def complete_loading(self, db):
        self.list_of_states = [State.load(db, key) for key in self.keys]

    def __repr__(self):
        return "[" + "\n".join([str(state) for state in self.list_of_states]) + "]"


class GitState(GitRepo, State):
    def __init__(self, path, diff, commit_hash=None):
        GitRepo.__init__(self, path)
        State.__init__(self)

        self.diff = diff
        self.commit_hash = commit_hash

    def apply(self, instance, db):
        print("""
Will now edit the repository {path}. To revert it back to its original state, please call:
    git reset --hard
    git checkout {original_hash}
    git stash pop
        """.format(original_hash=self.repo.head.commit.hexsha, path=self.path))

        self.repo.git.stash()
        self.repo.git.checkout(self.commit_hash)

        if self.diff.strip():
            with NamedTemporaryFile() as f:
                f.write(self.diff)
                print(self.diff)
                self.repo.git.apply(f.name)

    def __repr__(self):
        if self.diff:
            diff = "+dirty"
        else:
            diff = ""
        return "GitState ({self.path}): {self.commit_hash}{diff}".format(self=self, diff=diff)


class FileState(State):
    def apply(self, instance, db):
        raise NotImplementedError

    def __init__(self, file_path, file_content):
        State.__init__(self)

        self.file_path = file_path
        self.file_content = file_content

