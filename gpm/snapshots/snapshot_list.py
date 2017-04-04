from gpm.snapshots.base import BaseSnapshot


class SnapshotList(BaseSnapshot):
    def __init__(self, l=None):
        BaseSnapshot.__init__(self)
        self._list = l or []

    def append(self, snapshot):
        self._list.append(snapshot)

    def __iter__(self):
        return iter(self._list)