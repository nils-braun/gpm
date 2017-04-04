def store_commit(commit, db):
    output_file_id = db.store(commit._output_file_snapshot)
    dependency_id = db.store(commit._dependency_snapshots)

    full_store_id = db.store((output_file_id, dependency_id))

    db.add(commit.file_path, full_store_id)


def load_commit(commit_hash, db):
    output_file_id, dependency_id = db.get(commit_hash)

    output_file_snapshot = db.get(output_file_id)
    dependency_snapshots = db.get(dependency_id)

    return Commit(output_file_snapshot, dependency_snapshots, commit_hash)


class Commit:
    def __init__(self, output_file_snapshot, dependency_snapshots, commit_hash=None):
        self._output_file_snapshot = output_file_snapshot
        self._dependency_snapshots = dependency_snapshots
        self.commit_hash = commit_hash

    @property
    def file_path(self):
        return self._output_file_snapshot.file_path

    @property
    def file_content(self):
        return self._output_file_snapshot.file_content

    @property
    def states(self):
        return self._dependency_snapshots
