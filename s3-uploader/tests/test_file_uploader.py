from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

from gp2gp.fileuploader import FileUploader
from gp2gp.mesh import MeshFile


def test_upload():
    mock_s3 = MagicMock()
    uploader = FileUploader(mock_s3, "test_bucket")
    a_file = MeshFile(Path("test/file.dat"), datetime(2020, 3, 4, 8, 33))

    uploader.upload(a_file)

    mock_s3.upload_file.assert_called_once_with(
        Path("test/file.dat"), "test_bucket", "2020/03/04/file.dat"
    )
