from datetime import datetime
from pathlib import Path

from gp2gp.mesh import MeshInboxScanner, MeshFile


def test_finds_file_in_directory(fs):
    dat_file_path = Path("/IN/20201025030139_abc.dat")
    ctrl_file_path = Path("/IN/20201025030139_abc.ctrl")
    fs.create_dir("/IN")
    fs.create_file(dat_file_path, contents="I, am, data")
    fs.create_file(
        ctrl_file_path,
        contents=(
            "<DTSControl>"
            "<StatusRecord>"
            "<DateTime>"
            "20201025030139"
            "</DateTime>"
            "</StatusRecord>"
            "</DTSControl>"
        ),
    )

    expected = [MeshFile(path=dat_file_path, date_delivered=datetime(2020, 10, 25, 3, 1, 39))]

    scanner = MeshInboxScanner()

    result = list(scanner.scan("/IN"))

    assert result == expected
