from gpm.base.commit import load_commit
from gpm.db.database import Database


def get_commit(commit_hash):
    db = Database()

    return load_commit(commit_hash, db)


def get_results_for_file(file_name):
    db = Database()

    for commit_hash in db.get(file_name):
        yield load_commit(commit_hash, db)
