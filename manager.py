from contextlib import contextmanager

from gpm.config import ConfigObject
from gpm.state import ResultFolder
from gpm.db.state_database import KeyValueDatabase
from gpm.states.state import State
from gpm.utils.utils import get_state_file


class Calculation:
    def __init__(self, state_hash):
        self.state_hash = state_hash

        self._output_files = []

    @property
    def output_files(self):
        if not self._output_files:
            raise RuntimeError("Calculation has no output files added. Can not end calculation!")
        return self._output_files

    def add_output_file(self, output_file):
        self._output_files.append(output_file)


class GPM(ConfigObject):
    def __init__(self, base_dir, results_dir, externals):
        ConfigObject.__init__(self, base_dir)

        self.results_dir = ResultFolder(results_dir)
        self._externals = externals

        self._state_database = KeyValueDatabase(get_state_file(self.base_dir))

    @contextmanager
    def calculation(self):
        calculation = self._start_calculation()
        yield calculation
        # TODO: Do something special when it failed!
        self._end_calculation(calculation)

    def _start_calculation(self):
        # Snapshot the state of all dependencies (externals)
        state = self._externals.snapshot(self._state_database)
        # Store the snapshot state and get the hash, that describes this state uniquely
        state_hash = state.store(self._state_database)
        # Create a new calculation object based on this state
        calculation = Calculation(state_hash)
        # Return this calculation
        return calculation

    def _end_calculation(self, calculation):
        # Commit the new files with a reference to the state hash
        self.results_dir.commit(files=calculation.output_files,
                                commit_message="Finished calculation with "
                                               "{state_hash}".format(state_hash=calculation.state_hash))

    def get_states_for_file(self, result_file):
        commits = self.results_dir.get_commits(result_file)

        for commit in commits:
            commit_message = commit.message
            if commit_message.startswith("Finished calculation with "):
                yield State.load(self._state_database, commit_message[26:])

    def apply(self, state):
        state.apply(self._externals)

    def get_content_for_file(self, result_file):
        result_file = self.results_dir.normalize_file_name(result_file)
        commits = self.results_dir.get_commits(result_file)

        for commit in commits:
            commit_message = commit.message
            if commit_message.startswith("Finished calculation with "):
                yield State.load(self._state_database, commit_message[26:]), \
                      self.results_dir.repo.git.execute(["git", "show", commit.hexsha + ":" + result_file])