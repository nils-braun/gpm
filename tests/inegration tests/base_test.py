from unittest import TestCase
from tempfile import mkdtemp
import shutil
import os

from gpm import State, get_results_for_file

class IntegrationTestFixture(TestCase):
    def setUp(self):
        self.file_name = "my_file.dat"
        self.result_file_name = "result.dat"

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
        self.assertEqual(commit.file_content, "content 1")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.file_path, os.path.join(self.temp_file_folder, self.file_name))
            self.assertTrue(snapshot.file_content, "Some important stuff")

        commit = results[1]
        self.assertEqual(commit.file_path, os.path.join(self.temp_file_folder, self.result_file_name))
        self.assertEqual(commit.file_content, "content 2")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.file_path, os.path.join(self.temp_file_folder, self.file_name))
            self.assertTrue(snapshot.file_content, "Some important stuff")

        commit = results[2]
        self.assertEqual(commit.file_path, os.path.join(self.temp_file_folder, self.result_file_name))
        self.assertEqual(commit.file_content, "content 3")
        self.assertTrue(commit.commit_hash)
        for snapshot in commit.states:
            self.assertTrue(snapshot.file_path, os.path.join(self.temp_file_folder, self.file_name))
            self.assertTrue(snapshot.file_content, "Another stuff")
