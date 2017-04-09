import os
import shutil
from tempfile import mkdtemp
from subprocess import check_call

from unittest import TestCase


class IntegrationTestFixture(TestCase):
    def setUp(self):
        self.file_name = "my_file.dat"
        self.result_file_name = "result.dat"
        self.git_repo = "git_repo_dir"

        self.temp_file_folder = mkdtemp()
        os.chdir(self.temp_file_folder)

    def tearDown(self):
        shutil.rmtree(self.temp_file_folder)

    def calculate(self, state, content):
        with state.get_calculation() as calculation:
            with open(self.result_file_name, "w") as f:
                f.write(content)
            calculation.add_output_file(self.result_file_name)

    def change_file(self, content):
        with open(self.file_name, "w") as f:
            f.write(content)

    def change_repo(self, content, do_commit=True):
        if not os.path.isdir(self.git_repo):
            os.mkdir(self.git_repo)

        check_call(["git", "init"], cwd=self.git_repo)

        check_call(["git", "config", "user.email", "you@example.com"], cwd=self.git_repo)
        check_call(["git", "config", "user.name", "Your Name"], cwd=self.git_repo)

        with open(os.path.join(self.git_repo, "git_file"), "w") as f:
            f.write(content)

        if do_commit:
            check_call(["git", "add", "git_file"], cwd=self.git_repo)
            check_call(["git", "commit", "-m", "'A commit'"], cwd=self.git_repo)