import sqlite3
from datetime import datetime
from pathlib import Path

from gp2gp.mesh import MeshFile
from gp2gp.registry import ProcessedFileRegistry

A_PATH = Path("IN/a_file.dat")
A_DATE = datetime(2020, 1, 1)


def test_is_already_processed_returns_false_given_an_unprocessed_file():
    mesh_file = MeshFile(A_PATH, A_DATE)
    sqlite_conn = sqlite3.connect(":memory:")
    file_registry = ProcessedFileRegistry(sqlite_conn)

    expected = False

    actual = file_registry.is_already_processed(mesh_file)

    assert actual == expected


def test_is_already_processed_returns_true_given_a_processed_file():
    mesh_file = MeshFile(A_PATH, A_DATE)

    sqlite_conn = sqlite3.connect(":memory:")
    file_registry = ProcessedFileRegistry(sqlite_conn)

    expected = True

    file_registry.mark_processed(mesh_file)
    actual = file_registry.is_already_processed(mesh_file)

    assert actual == expected
