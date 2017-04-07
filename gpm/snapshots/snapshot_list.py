from gpm.snapshots.base import BaseSnapshot


class SnapshotList(BaseSnapshot):
    def __init__(self, l=None):
        BaseSnapshot.__init__(self)

        if l:
            self._list = {str(item): item for item in l}
        else:
            self._list = {}

    def append(self, snapshot):
        self._list[str(snapshot)] = snapshot

    def __iter__(self):
        return iter(self._list.values())