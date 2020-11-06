class MeshS3Uploader:
    def __init__(self, s3, bucket_name):
        self._s3 = s3
        self._bucket_name = bucket_name

    def upload(self, mesh_file):
        key = f"{mesh_file.date_delivered.strftime('%Y/%m/%d')}/{mesh_file.path.name}"
        self._s3.upload_file(mesh_file.path, self._bucket_name, key)
