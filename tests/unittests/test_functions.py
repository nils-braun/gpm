from gpm.fixtures import IntegrationTestFixture

from gpm.snapshots.creator import create_snapshot
from gpm.snapshots.file_snapshot import FileSnapshot


class FunctionsTestCase(IntegrationTestFixture):
    def test_create_snapshot(self):
        with open(self.file_name, "w") as f:
            f.write("test")

        file_snapshot = create_snapshot(self.file_name)
        self.assertIsInstance(file_snapshot, FileSnapshot)

        created_file_snapshot = FileSnapshot(self.file_name)
        file_snapshot = create_snapshot(created_file_snapshot)
        self.assertIs(file_snapshot, created_file_snapshot)

        self.assertRaises(AttributeError, create_snapshot, "another_file.py")