from pathlib import Path

from gp2gp.mesh.inbox import MeshInboxScanner
from gp2gp.mesh.file import MeshFile


def test_finds_file_in_directory(fs):
    dat_file_path = Path("/IN/20201025030139_abc.dat")
    fs.create_dir("/IN")
    fs.create_file(dat_file_path, contents="I, am, data")

    expected = [MeshFile(path=dat_file_path)]

    scanner = MeshInboxScanner()

    result = list(scanner.scan("/IN"))

    assert result == expected
