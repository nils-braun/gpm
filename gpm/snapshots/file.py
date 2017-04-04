import os
import stat
from datetime import datetime

from gpm.snapshots.base import BaseSnapshot


class FileSnapshot(BaseSnapshot):
    def __init__(self, file_path, store_content=True):
        BaseSnapshot.__init__(self)

        self.file_path = os.path.abspath(file_path)

        if store_content:
            with open(self.file_path, "rb") as f:
                self.file_content = f.read()
        else:
            self.file_content = None

        self.last_modified = datetime.fromtimestamp(os.stat(self.file_path)[stat.ST_MTIME])
