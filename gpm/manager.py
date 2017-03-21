import os
from contextlib import contextmanager

from gpm.config import ConfigObject
from results.result import ResultFolder
from gpm.db.state_database import KeyValueDatabase
from gpm.utils.utils import get_state_file, get_results_file


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
        self._output_files.append(os.path.abspath(output_file))


class GPM(ConfigObject):
    def __init__(self, base_dir, externals):
        ConfigObject.__init__(self, base_dir)

        self._externals = externals

        self._state_database = KeyValueDatabase(get_state_file(self.base_dir))

        self.results_dir = ResultFolder(self._state_database)

    @contextmanager
    def get_calculation(self):
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
        for output_file_name in calculation.output_files:
            self.results_dir.store_results(output_file_name, calculation.state_hash)

    def get_results_for_file(self, result_file):
        return self.results_dir.get_results(result_file)

    def apply(self, state):
        state.apply(self._externals, self._state_database)