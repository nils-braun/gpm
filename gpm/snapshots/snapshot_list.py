from gpm.snapshots.base import BaseSnapshot


class SnapshotList(BaseSnapshot):
    def __init__(self, l=None):
        BaseSnapshot.__init__(self)

        if l:
            self._list = {item.name: item for item in l}
        else:
            self._list = {}

    def append(self, snapshot):
        self._list[snapshot.name] = snapshot

    def __iter__(self):
        return iter(self._list.values())

    @property
    def name_params(self):
        return len(self._list)

    def __eq__(self, other):
        return other._list == self._list