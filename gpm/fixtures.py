import os
import shutil
from tempfile import mkdtemp
from unittest import TestCase


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