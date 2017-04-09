import os

from gpm import State, get_results_for_file, get_commit
from gpm.fixtures import IntegrationTestFixture


class BaseIntegrationTestCase(IntegrationTestFixture):
    def test_base_file_functionality(self):
        state = State()

        self.change_file("Some important stuff")
        state.snapshot(self.file_name)
        self.calculate(state, "content 1")

        self.change_file("Another stuff")
        self.calculate(state, "content 2")

        state.snapshot(self.file_name)
        self.change_file("Should not be visible")
        self.calculate(state, "content 3")

        results = list(get_results_for_file(self.result_file_name))

        self.assertEqual(len(results), 3)

        commit = results[0]
        self.assertEqual(commit.file_path, os.path.join(self.temp_file_folder, self.result_file_name))
        self.assertEqual(commit.file_content, b"content 1")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.file_path, os.path.join(self.temp_file_folder, self.file_name))
            self.assertTrue(snapshot.file_content, b"Some important stuff")
        self.assertEqual(get_commit(commit.commit_hash), commit)

        commit = results[1]
        self.assertEqual(commit.file_path, os.path.join(self.temp_file_folder, self.result_file_name))
        self.assertEqual(commit.file_content, b"content 2")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.file_path, os.path.join(self.temp_file_folder, self.file_name))
            self.assertTrue(snapshot.file_content, b"Some important stuff")
        self.assertEqual(get_commit(commit.commit_hash), commit)

        commit = results[2]
        self.assertEqual(commit.file_path, os.path.join(self.temp_file_folder, self.result_file_name))
        self.assertEqual(commit.file_content, b"content 3")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.file_path, os.path.join(self.temp_file_folder, self.file_name))
            self.assertTrue(snapshot.file_content, b"Another stuff")
        self.assertEqual(get_commit(commit.commit_hash), commit)
