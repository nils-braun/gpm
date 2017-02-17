from gpm.utils.git_utils import GitRepo


class ResultFolder(GitRepo):
    def __init__(self, path):
        GitRepo.__init__(self, path, allowed_to_create=True)

    def commit(self, files, commit_message):
        self.repo.index.add(files)

        if (not self.repo.head.is_valid() or
                self.repo.index.diff(self.repo.head.commit) or
                self.repo.head.commit.message != commit_message):
            self.repo.index.commit(commit_message)

    def get_commits(self, result_file):
        result_file = self.normalize_file_name(result_file)
        return self.repo.iter_commits(paths=result_file)

    def normalize_file_name(self, result_file):
        return result_file.replace(self.path, "")



