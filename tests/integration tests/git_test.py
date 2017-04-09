import os

from gpm import State, get_results_for_file, get_commit
from gpm.fixtures import IntegrationTestFixture


class GitIntegrationTestCase(IntegrationTestFixture):
    def test_base_git_functionality(self):
        state = State()

        self.change_repo("Some important stuff", do_commit=True)
        state.snapshot(self.git_repo)
        self.calculate(state, "content 1")

        self.change_repo("Another stuff", do_commit=False)
        state.snapshot(self.git_repo)
        self.calculate(state, "content 2")

        state.snapshot(self.git_repo)
        self.change_repo("Should not be visible", do_commit=True)
        self.calculate(state, "content 3")

        results = list(get_results_for_file(self.result_file_name))

        self.assertEqual(len(results), 3)

        commit = results[0]
        self.assertEqual(commit.file_path, os.path.join(self.temp_file_folder, self.result_file_name))
        self.assertEqual(commit.file_content, b"content 1")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.path, os.path.join(self.temp_file_folder, self.git_repo))
        self.assertEqual(get_commit(commit.commit_hash), commit)

        commit = results[1]
        self.assertEqual(commit.file_path, os.path.join(self.temp_file_folder, self.result_file_name))
        self.assertEqual(commit.file_content, b"content 2")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.path, os.path.join(self.temp_file_folder, self.git_repo))
        self.assertEqual(get_commit(commit.commit_hash), commit)

        commit = results[2]
        self.assertEqual(commit.file_path, os.path.join(self.temp_file_folder, self.result_file_name))
        self.assertEqual(commit.file_content, b"content 3")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.path, os.path.join(self.temp_file_folder, self.git_repo))
        self.assertEqual(get_commit(commit.commit_hash), commit)
