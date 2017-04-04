from gpm.db.key_value_db import KeyValueDB
from gpm.snapshots.snapshot_list import SnapshotList

try:
    import cPickle as cpickle
except ImportError:
    import pickle

from hashlib import md5


class SnapshotListStorer:
    def __init__(self, snapshot_list, db):
        self.snapshot_list_ids = [db.store(snapshot) for snapshot in snapshot_list]


class Database:
    def __init__(self, db_folder=None):
        self._db_implementation = KeyValueDB(db_folder)

    def get(self, key):
        value = pickle.loads(self._db_implementation[key])

        if isinstance(value, SnapshotListStorer):
            value = SnapshotList([self.get(snapshot_id) for snapshot_id in value.snapshot_list_ids])

        return value

    def store(self, key_or_item, item_or_none = None):
        if item_or_none is None:
            item = key_or_item
            key = None
        else:
            item = item_or_none
            key = key_or_item

        if isinstance(item, SnapshotList):
            item = SnapshotListStorer(item, self)

        pickled_item = pickle.dumps(item)

        if key is None:
            key = md5(pickled_item).hexdigest()

        self._db_implementation[key] = pickled_item

        return key

    def add(self, key, item):
        try:
            l = self.get(key)
        except KeyError:
            l = []

        l.append(item)
        self.store(key, l)