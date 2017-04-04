from gpm.snapshots.base import BaseSnapshot


class SnapshotList(BaseSnapshot):
    def __init__(self):
        BaseSnapshot.__init__(self)
        self._list = []

    def append(self, snapshot):
        self._list.append(snapshot)
