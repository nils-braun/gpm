import os

try:
    import cPickle as pickle
except ImportError:
    import pickle
from hashlib import md5
import simplejson


class KeyValueDatabase:
    def __init__(self, database_file):
        self.database_file = database_file
        self._database = {}

        if os.path.exists(database_file):
            self._load_db()

    def _load_db(self):
        with open(self.database_file, 'rb') as f:
            self._database = simplejson.load(f)

    def _store_db(self):
        with open(self.database_file, 'wb') as f:
            simplejson.dump(self._database, f)

    def set(self, key_or_value, value_or_none=None):
        if value_or_none is None:
            value = key_or_value
            key = None
        else:
            value = value_or_none
            key = key_or_value

        string_to_store = pickle.dumps(value)

        if key is None:
            key = md5(string_to_store).hexdigest()

        self._database[key] = string_to_store
        self._store_db()

        return key

    def get(self, key):
        self._load_db()

        value_as_string = self._database[key]
        value = pickle.loads(value_as_string)

        return value
