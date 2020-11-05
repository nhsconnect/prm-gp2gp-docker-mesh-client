from dataclasses import dataclass
from datetime import datetime

import boto3


class MIToS3Uploader:

    def __init__(self, mesh_inbox_scanner, file_registry, file_uploader):
        self._mesh_inbox_scanner = mesh_inbox_scanner
        self._file_registry = file_registry
        self._file_uploader = file_uploader

    def run(self, directory_path, s3_bucket):
        mesh_files = self._mesh_inbox_scanner.scan(directory_path)

        for file in mesh_files:
            if not self._file_registry.is_already_processed(file, s3_bucket):
                self._file_uploader.upload(file, s3_bucket)
                self._file_registry.mark_processed(file, s3_bucket)


@dataclass(frozen=True)
class MeshFile:
    path: str
    date_delivered: datetime
