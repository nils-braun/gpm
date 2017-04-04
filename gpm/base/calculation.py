from gpm.snapshots.creator import create_snapshot
from gpm.base.commit import Commit, store_commit


class Calculation:
    def __init__(self, dependency_snapshots, db):
        self._dependency_snapshots = dependency_snapshots
        self._db = db

        self.output_files = []

    def start(self):
        pass

    def end(self):
        for output_file in self.output_files:
            output_file_snapshot = create_snapshot(output_file)
            dependency_snapshots = self._dependency_snapshots

            commit = Commit(output_file_snapshot, dependency_snapshots)
            store_commit(commit, self._db)

    def add_output_file(self, output_file):
        self.output_files.append(output_file)
