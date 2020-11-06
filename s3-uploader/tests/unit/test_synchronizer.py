from datetime import datetime
from pathlib import Path

from gp2gp.synchronizer import MeshToS3Synchronizer
from gp2gp.mesh import MeshFile
from unittest.mock import MagicMock, call

A_DATE = datetime(2020, 10, 25)


def test_uploads_file():
    mock_mesh_inbox_scanner = MagicMock()
    mock_file_registry = MagicMock()
    mock_file_uploader = MagicMock()

    mock_mesh_file = MeshFile(Path("path/to/file.dat"), date_delivered=A_DATE)

    mock_mesh_inbox_scanner.scan.return_value = [mock_mesh_file]
    mock_file_registry.is_already_processed.return_value = False

    uploader = MeshToS3Synchronizer(mock_mesh_inbox_scanner, mock_file_registry, mock_file_uploader)

    uploader.run("fake/path", "fake-bucket")

    mock_mesh_inbox_scanner.scan.assert_called_once_with("fake/path")
    mock_file_uploader.upload.assert_called_once_with(mock_mesh_file)


def test_uploads_multiple_files():
    mock_mesh_inbox_scanner = MagicMock()
    mock_file_registry = MagicMock()
    mock_file_uploader = MagicMock()

    mock_mesh_file = MeshFile(path=Path("path/to/file.dat"), date_delivered=A_DATE)
    mock_second_mesh_file = MeshFile(path=Path("path/to/secondfile.dat"), date_delivered=A_DATE)

    mock_mesh_inbox_scanner.scan.return_value = [mock_mesh_file, mock_second_mesh_file]
    mock_file_registry.is_already_processed.return_value = False

    uploader = MeshToS3Synchronizer(mock_mesh_inbox_scanner, mock_file_registry, mock_file_uploader)

    uploader.run("fake/path", "fake-bucket")

    mock_mesh_inbox_scanner.scan.assert_called_once_with("fake/path")

    calls = [call(mock_mesh_file), call(mock_second_mesh_file)]
    mock_file_uploader.upload.assert_has_calls(calls)


class MockFileRegistry:
    def __init__(self):
        self.registry = set()

    def mark_processed(self, filename):
        self.registry.add(filename)

    def is_already_processed(self, filename):
        return filename in self.registry


def mock_registry(already_processed):
    mock_file_registry = MockFileRegistry()

    for filename in already_processed:
        mock_file_registry.mark_processed(filename)

    return mock_file_registry


def test_only_uploads_new_files():

    mock_new_file = MeshFile(path=Path("path/to/newfile.dat"), date_delivered=A_DATE)
    mock_old_file = MeshFile(path=Path("path/to/oldfile.dat"), date_delivered=A_DATE)

    mock_mesh_inbox_scanner = MagicMock()
    mock_file_registry = mock_registry(already_processed=[mock_old_file])
    mock_file_uploader = MagicMock()

    mock_mesh_inbox_scanner.scan.return_value = [mock_new_file, mock_old_file]

    uploader = MeshToS3Synchronizer(mock_mesh_inbox_scanner, mock_file_registry, mock_file_uploader)

    uploader.run("fake/path", "fake-bucket")

    mock_mesh_inbox_scanner.scan.assert_called_once_with("fake/path")

    mock_file_uploader.upload.assert_called_once_with(
        MeshFile(path=Path("path/to/newfile.dat"), date_delivered=A_DATE)
    )


def test_uploads_file_only_once():

    mock_mesh_inbox_scanner = MagicMock()
    mock_file_registry = MockFileRegistry()
    mock_file_uploader = MagicMock()

    mock_mesh_file = MeshFile(path=Path("path/to/file.dat"), date_delivered=A_DATE)

    mock_mesh_inbox_scanner.scan.return_value = [mock_mesh_file]

    uploader = MeshToS3Synchronizer(mock_mesh_inbox_scanner, mock_file_registry, mock_file_uploader)

    uploader.run("fake/path", "fake-bucket")
    uploader.run("fake/path", "fake-bucket")

    mock_file_uploader.upload.assert_called_once_with(mock_mesh_file)
