from datetime import datetime

from gp2gp.uploader import MeshToS3Uploader, MeshFile
from unittest.mock import MagicMock, call

A_DATE = datetime(2020, 10, 25)


def test_uploads_file():
    mock_mesh_inbox_scanner = MagicMock()
    mock_file_registry = MagicMock()
    mock_file_uploader = MagicMock()

    mock_mesh_file = MeshFile(path="path/to/file.dat", date_delivered=A_DATE)

    mock_mesh_inbox_scanner.scan.return_value = [mock_mesh_file]
    mock_file_registry.is_already_processed.return_value = False

    uploader = MeshToS3Uploader(mock_mesh_inbox_scanner, mock_file_registry, mock_file_uploader)

    uploader.run("fake/path", "fake-bucket")

    mock_mesh_inbox_scanner.scan.assert_called_once_with("fake/path")
    mock_file_uploader.upload.assert_called_once_with(mock_mesh_file, "fake-bucket")


def test_uploads_multiple_files():
    mock_mesh_inbox_scanner = MagicMock()
    mock_file_registry = MagicMock()
    mock_file_uploader = MagicMock()

    mock_mesh_file = MeshFile(path="path/to/file.dat", date_delivered=A_DATE)
    mock_second_mesh_file = MeshFile(path="path/to/secondfile.dat", date_delivered=A_DATE)

    mock_mesh_inbox_scanner.scan.return_value = [mock_mesh_file, mock_second_mesh_file]
    mock_file_registry.is_already_processed.return_value = False

    uploader = MeshToS3Uploader(mock_mesh_inbox_scanner, mock_file_registry, mock_file_uploader)

    uploader.run("fake/path", "fake-bucket")

    mock_mesh_inbox_scanner.scan.assert_called_once_with("fake/path")

    calls = [call(mock_mesh_file, "fake-bucket"), call(mock_second_mesh_file, "fake-bucket")]
    mock_file_uploader.upload.assert_has_calls(calls)


class MockFileRegistry:
    def __init__(self):
        self.registry = set()

    def mark_processed(self, file, bucket):
        self.registry.add((file, bucket))

    def is_already_processed(self, file, bucket):
        return (file, bucket) in self.registry


def mock_registry(already_processed):
    mock_file_registry = MockFileRegistry()

    for file, bucket in already_processed:
        mock_file_registry.mark_processed(file, bucket)

    return mock_file_registry


def test_only_uploads_new_files():

    mock_new_file = MeshFile(path="path/to/newfile.dat", date_delivered=A_DATE)
    mock_old_file = MeshFile(path="path/to/oldfile.dat", date_delivered=A_DATE)

    mock_mesh_inbox_scanner = MagicMock()
    mock_file_registry = mock_registry(already_processed={(mock_old_file, "fake-bucket")})
    mock_file_uploader = MagicMock()

    mock_mesh_inbox_scanner.scan.return_value = [mock_new_file, mock_old_file]

    uploader = MeshToS3Uploader(mock_mesh_inbox_scanner, mock_file_registry, mock_file_uploader)

    uploader.run("fake/path", "fake-bucket")

    mock_mesh_inbox_scanner.scan.assert_called_once_with("fake/path")

    mock_file_uploader.upload.assert_called_once_with(
        MeshFile(path="path/to/newfile.dat", date_delivered=A_DATE), "fake-bucket"
    )


def test_uploads_file_only_once():

    mock_mesh_inbox_scanner = MagicMock()
    mock_file_registry = MockFileRegistry()
    mock_file_uploader = MagicMock()

    mock_mesh_file = MeshFile(path="path/to/file.dat", date_delivered=A_DATE)

    mock_mesh_inbox_scanner.scan.return_value = [mock_mesh_file]

    uploader = MeshToS3Uploader(mock_mesh_inbox_scanner, mock_file_registry, mock_file_uploader)

    uploader.run("fake/path", "fake-bucket")
    uploader.run("fake/path", "fake-bucket")

    mock_file_uploader.upload.assert_called_once_with(mock_mesh_file, "fake-bucket")
