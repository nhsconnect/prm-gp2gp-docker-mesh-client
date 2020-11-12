from datetime import datetime
from pathlib import Path

from gp2gp.mesh.file import MeshFile, MeshFileException
from pytest import raises


def test_reads_delivery_date(fs):
    dat_file_path = Path("/IN/20201025030139_abc.dat")
    ctl_file_path = Path("/IN/20201025030139_abc.ctl")
    fs.create_dir("/IN")
    fs.create_file(dat_file_path, contents="I, am, data")
    fs.create_file(
        ctl_file_path,
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

    mesh_file = MeshFile(path=dat_file_path)

    result = mesh_file.read_delivery_date()
    expected_date = datetime(2020, 10, 25, 3, 1, 39)

    assert result == expected_date


def test_throws_exception_given_invalid_ctrl_file(fs):
    dat_file_path = Path("/IN/20201025030139_abc.dat")
    ctl_file_path = Path("/IN/20201025030139_abc.ctl")
    fs.create_dir("/IN")
    fs.create_file(dat_file_path, contents="I, am, data")
    fs.create_file(
        ctl_file_path,
        contents="<Data>NotValidData</Data>",
    )

    mesh_file = MeshFile(path=dat_file_path)

    with raises(MeshFileException):
        mesh_file.read_delivery_date()


def test_throws_exception_given_non_xml_ctrl_file(fs):
    dat_file_path = Path("/IN/20201025030139_abc.dat")
    ctl_file_path = Path("/IN/20201025030139_abc.ctl")
    fs.create_dir("/IN")
    fs.create_file(dat_file_path, contents="I, am, data")
    fs.create_file(
        ctl_file_path,
        contents="This is not xml",
    )

    mesh_file = MeshFile(path=dat_file_path)

    with raises(MeshFileException):
        mesh_file.read_delivery_date()
