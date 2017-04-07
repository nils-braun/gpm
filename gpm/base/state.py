from contextlib import contextmanager

from gpm.base.commit import store_commit, Commit
from gpm.snapshots.snapshot_list import SnapshotList
from gpm.db.database import Database
from gpm.snapshots.creator import create_snapshot
from gpm.base.calculation import Calculation


class State:
    def __init__(self, database_dir=None):
        self.snapshots = SnapshotList()
        self.db = Database(database_dir)

    def snapshot(self, snapshot_stub):
        snapshot = create_snapshot(snapshot_stub)
        self.snapshots.append(snapshot)

    @contextmanager
    def get_calculation(self):
        calculation = Calculation()

        yield calculation

        for output_file in calculation.output_files:
            output_file_snapshot = create_snapshot(output_file)
            dependency_snapshots = self.snapshots

            commit = Commit(output_file_snapshot, dependency_snapshots)
            store_commit(commit, self.db)
