from contextlib import contextmanager

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
        calculation = Calculation(self.snapshots, self.db)

        calculation.start()
        yield calculation
        calculation.end()