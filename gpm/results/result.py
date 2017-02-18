import os

from simplejson import OrderedDict

from gpm.instances.instance import FileInstance
from gpm.states.state import State


class ResultFolder:
    def __init__(self, state_db):
        self._state_db = state_db

    def store_results(self, output_file_name, state_hash):
        output_file_state = FileInstance(output_file_name).snapshot(self._state_db)
        output_file_hash = output_file_state.store(self._state_db)

        try:
            stored_state_content_pairs = self._state_db.get(output_file_name)
        except KeyError:
            stored_state_content_pairs = OrderedDict()

        if state_hash in stored_state_content_pairs:
            if stored_state_content_pairs[state_hash] != output_file_hash:
                raise RuntimeError("It seems that you have produced different output file contents "
                                   "based on the same status!")
            else:
                return

        # We only need to store something, if it was not already there
        stored_state_content_pairs[state_hash] = output_file_hash

        self._state_db.set(output_file_name, stored_state_content_pairs)

    def get_results(self, result_file_name):
        result_file_name = os.path.abspath(result_file_name)

        stored_state_content_pairs = self._state_db.get(result_file_name)

        for state_hash, output_file_hash in stored_state_content_pairs.items():
            yield Commit(result_file_name, output_file_hash, state_hash, self._state_db)


class Commit:
    def __init__(self, file_name, file_content_hash, state_hash, state_db):
        self.file_name = file_name
        self._file_content_hash = file_content_hash
        self._state_hash = state_hash

        self._state_db = state_db

    @property
    def file_content(self):
        from gpm.states.state import FileState

        file_state = State.load(self._state_db, self._file_content_hash)

        assert isinstance(file_state, FileState)

        return file_state.file_content

    @property
    def state(self):
        return State.load(self._state_db, self._state_hash)