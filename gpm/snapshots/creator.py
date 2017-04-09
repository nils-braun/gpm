from gpm.snapshots.base import BaseSnapshot
from gpm.snapshots.file_snapshot import FileSnapshot
from gpm.snapshots.git_snapshot import GitSnapshot

import os


def create_snapshot(snapshot_stub):
    if isinstance(snapshot_stub, BaseSnapshot):
        return snapshot_stub
    elif os.path.exists(snapshot_stub):
        if os.path.isdir(snapshot_stub):
            return GitSnapshot(snapshot_stub)
        else:
            return FileSnapshot(snapshot_stub)
    else:
        raise AttributeError
