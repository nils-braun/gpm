import os

from gpm import State, get_results_for_file, get_commit
from gpm.fixtures import IntegrationTestFixture


class CheckoutIntegrationTestCase(IntegrationTestFixture):
    def test_base_file_functionality(self):
        state = State()

        self.change_file("Some important stuff")
        state.snapshot(self.file_name)
        self.calculate(state, "content 1")

        self.change_file("Another stuff")
        state.snapshot(self.file_name)
        self.calculate(state, "content 2")

        commits = get_results_for_file(self.result_file_name)

        for commit in commits:
            with commit.checkout() as f:
                self.assertTrue(os.path.exists(f.name))
                self.assertEqual(f.read(), commit.file_content)