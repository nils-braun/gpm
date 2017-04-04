from gpm.snapshots.base import BaseSnapshot
from gpm.snapshots.file import FileSnapshot

import os


def create_snapshot(snapshot_stub):
    if isinstance(snapshot_stub, BaseSnapshot):
        return snapshot_stub
    elif os.path.exists(snapshot_stub):
        return FileSnapshot(snapshot_stub)
    else:
        raise AttributeError
