from pathlib import Path

from gp2gp.mesh.file import MeshFile


class MeshInboxScanner:
    def scan(self, directory):
        directory_path = Path(directory)

        file_paths = directory_path.glob("*.dat")

        for file_path in file_paths:
            yield MeshFile(path=file_path)
